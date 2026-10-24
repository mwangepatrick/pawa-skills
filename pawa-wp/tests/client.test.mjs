import test from 'node:test';
import assert from 'node:assert/strict';
import { PawaWpClient } from '../src/client.mjs';

const type = { slug: 'ht_kb', rest_base: 'articles', rest_namespace: 'wp/v2', taxonomies: ['kb_category'] };
const taxonomies = { kb_category: { rest_base: 'article-categories', rest_namespace: 'wp/v2', types: ['ht_kb'], hierarchical: true } };
const article = { id: 150, type: 'ht_kb', status: 'publish', slug: 'existing', title: { raw: 'Title' }, content: { raw: '<p>Body</p>' }, excerpt: { raw: 'Summary' }, kb_category: [6], modified_gmt: '2026-10-13T10:00:00', link: 'https://docs.cosmopawa.com/knowledge-base/existing/' };
const response = (data, status = 200, headers = {}) => new Response(JSON.stringify(data), { status, headers: { 'Content-Type': 'application/json', ...headers } });
function fixture(handler, options = {}) {
  const calls = [];
  const client = new PawaWpClient({ username: 'test', password: 'synthetic-secret', allowWrites: true, ...options, fetchImpl: async (url, init) => {
    const u = new URL(url); calls.push({ u, init });
    if (u.pathname.endsWith('/types/ht_kb')) return response(type);
    if (u.pathname.endsWith('/taxonomies')) return response(taxonomies);
    if (init.method === 'OPTIONS') return response({schema:{properties:{'article-categories':{type:'array',items:{type:'integer'}}}}});
    return handler(u, init, calls);
  }});
  return { client, calls };
}
test('fixed target and discovery use actual custom REST base and taxonomy field', async () => {
  const {client, calls} = fixture(u => response(u.pathname.endsWith('/article-categories') ? [{id: 6, name: 'Front Office'}] : []));
  assert.equal((await client.discover()).article.rest_base, 'articles');
  assert.deepEqual((await client.categories()).items.map(t => t.id), [6]);
  assert.ok(calls.every(c => c.u.origin === 'https://docs.cosmopawa.com'));
  assert.ok(calls.every(c => c.init.redirect === 'error'));
});
test('connection output excludes credentials and distinguishes authenticated edit access', async () => {
  const {client} = fixture(u => response(u.pathname.endsWith('/users/me') ? {id: 1, capabilities: {edit_posts: true}} : []));
  const result = await client.verifyConnection();
  assert.equal(result.authenticated, true);
  assert.equal(result.edit_access, true);
  assert.equal(result.publish_access, 'unverified');
  assert.ok(!JSON.stringify(result).includes('synthetic-secret'));
});
test('search reads every page and does not silently claim full visibility', async () => {
  const {client, calls} = fixture(u => response([{...article, id: Number(u.searchParams.get('page'))}], 200, {'X-WP-TotalPages': '2'}));
  const result = await client.search({slug: 'existing', statuses: ['publish']});
  assert.equal(result.complete, true); assert.equal(result.items.length, 2);
  assert.equal(calls.filter(c => c.u.pathname.endsWith('/articles') && c.init.method==='GET').length, 2);
});
test('draft create explicitly sends slug excerpt taxonomy IDs and verifies read-back', async () => {
  let saved;
  const {client, calls} = fixture((u, init) => {
    if (init.method === 'POST') { saved = JSON.parse(init.body); return response({...article, id: 151, ...saved}); }
    if (u.pathname.endsWith('/article-categories')) return response([{id:6}]);
    return response({...article, id:151, ...saved, title:{raw:saved.title}, content:{raw:saved.content}, excerpt:{raw:saved.excerpt}});
  });
  const result = await client.createDraft({title:'Title', content:'<p>Body</p>', slug:'new-guide', excerpt:'Summary', categories:[6]});
  assert.equal(saved.status,'draft'); assert.deepEqual(saved['article-categories'],[6]); assert.equal(saved.slug,'new-guide');
  assert.equal(result.verified,true); assert.equal(result.article.id,151);
  assert.equal(calls.filter(c=>c.init.method==='POST').length,1);
});
test('writes disabled by default', async () => {
  const {client,calls} = fixture(()=>response(article),{allowWrites:false});
  await assert.rejects(client.publish({id:150,expected_modified_gmt:article.modified_gmt,intent:'publish'}),/Writes disabled/);
  assert.equal(calls.filter(c=>c.init.method==='POST').length,0);
});
test('draft-only update of published article and stale writes are rejected', async () => {
  const {client,calls} = fixture(()=>response(article));
  await assert.rejects(client.update({id:150,expected_modified_gmt:article.modified_gmt,intent:'draft',content:'changed'}),/published article/);
  await assert.rejects(client.update({id:150,expected_modified_gmt:'old',intent:'live_update',content:'changed'}),/changed/);
  assert.equal(calls.filter(c=>c.init.method==='POST').length,0);
});
test('ambiguous writes are not retried and sensitive error text is omitted', async () => {
  const {client,calls} = fixture((u,init)=> {
    if(init.method==='POST') throw new Error('synthetic-secret');
    return response([{id:6}]);
  });
  await assert.rejects(client.createDraft({title:'Title',content:'Body',slug:'new-guide',excerpt:'Summary',categories:[6]}),e=>e.code==='WRITE_UNCERTAIN' && !e.message.includes('synthetic-secret'));
  assert.equal(calls.filter(c=>c.init.method==='POST').length,1);
});
test('malicious discovered routes cannot redirect credentialed requests', async () => {
  const client=new PawaWpClient({fetchImpl:async()=>response({...type,rest_base:'../users'})});
  await assert.rejects(client.discover(),/route/);
});
test('publish requires explicit intent and read-back checks status', async () => {
  let published=false;
  const {client}=fixture((u,init)=> { if(init.method==='POST'){published=true;return response(article);} return response({...article,status:published?'publish':'draft'}); });
  await assert.rejects(client.publish({id:150,expected_modified_gmt:article.modified_gmt,intent:'draft'}),/intent/);
  const result=await client.publish({id:150,expected_modified_gmt:article.modified_gmt,intent:'publish'});
  assert.equal(result.verified,true); assert.equal(result.browser_verification,'required');
});
test('null write response reports uncertain persistence and never retries', async()=>{
  const {client,calls}=fixture((u,init)=>init.method==='POST'?response(null):response([{id:6}]));
  await assert.rejects(client.createDraft({title:'Title',content:'Body',slug:'new-guide',excerpt:'Summary',categories:[6]}),e=>e.code==='WRITE_UNCERTAIN');
  assert.equal(calls.filter(c=>c.init.method==='POST').length,1);
});
test('edit-context output omits article passwords and unrelated metadata',async()=>{
  const {client}=fixture(()=>response({...article,password:'private-article-password',meta:{secret:'hidden'},author:99}));
  const result=await client.read({id:150});
  assert.ok(!JSON.stringify(result).includes('private-article-password'));
  assert.equal(result.meta,undefined); assert.equal(result.author,undefined);
});
test('denied status search and server errors report limits without raw body',async()=>{
  const {client}=fixture(()=>response({message:'synthetic-secret'},403));
  const result=await client.search({statuses:['private']});
  assert.equal(result.complete,false); assert.equal(result.unavailable_statuses[0].error_code,'HTTP_403');
  assert.ok(!JSON.stringify(result).includes('synthetic-secret'));
});
test('schema mismatch blocks category writes before a POST',async()=>{
  const client=new PawaWpClient({username:'test',password:'synthetic-secret',allowWrites:true,fetchImpl:async(url,init)=>{
    const path=new URL(url).pathname;
    if(path.endsWith('/types/ht_kb'))return response(type);
    if(path.endsWith('/taxonomies'))return response(taxonomies);
    return response({schema:{properties:{kb_category:{type:'array'}}}});
  }});
  await assert.rejects(client.createDraft({title:'Title',content:'Body',slug:'new-guide',excerpt:'Summary',categories:[6]}),e=>e.code==='TAXONOMY_FIELD_INVALID');
});
