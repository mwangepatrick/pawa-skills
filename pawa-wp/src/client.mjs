const ORIGIN = 'https://docs.cosmopawa.com';
const STATUSES = ['publish', 'draft', 'pending', 'private'];
export class WpError extends Error {
  constructor(code, message) { super(message); this.code = code; }
}
export class PawaWpClient {
  constructor({username = '', password = '', allowWrites = false, categoryTaxonomy = '', fetchImpl = fetch} = {}) {
    this.username = username; this.password = password; this.allowWrites = allowWrites;
    this.categoryTaxonomy = categoryTaxonomy; this.fetch = fetchImpl;
  }
  connectionStatus() {
    return {site: 'pawa-docs', origin: ORIGIN, credentials_present: Boolean(this.username && this.password), writes_enabled: this.allowWrites, scope: 'ht_kb documentation only'};
  }
  async request(path, {method = 'GET', body, auth = true} = {}) {
    const readOnly = method === 'GET' || method === 'OPTIONS';
    if (!path.startsWith('/wp-json/') || path.includes('..') || path.includes('\\')) throw new WpError('ROUTE_INVALID', 'Invalid REST route');
    const url = new URL(path, ORIGIN);
    if (url.origin !== ORIGIN) throw new WpError('ROUTE_INVALID', 'Invalid REST origin');
    const headers = {'Content-Type':'application/json'};
    if (auth && this.username && this.password) headers.Authorization = `Basic ${Buffer.from(`${this.username}:${this.password}`).toString('base64')}`;
    let res;
    try {
      res = await this.fetch(url.href, {method, headers, redirect:'error', signal:AbortSignal.timeout(15000), ...(body === undefined ? {} : {body:JSON.stringify(body)})});
    } catch {
      throw new WpError(readOnly ? 'CONNECTION_FAILED' : 'WRITE_UNCERTAIN', readOnly ? 'REST connection failed; no credentials or server details returned' : 'Write response unavailable; reconcile before retrying');
    }
    if (!res.ok) throw new WpError(!readOnly && res.status >= 500 ? 'WRITE_UNCERTAIN' : `HTTP_${res.status}`, `REST ${method} returned HTTP ${res.status}${!readOnly && res.status >= 500 ? '; reconcile before retrying' : ''}`);
    let data;
    try { data = await res.json(); }
    catch { throw new WpError(readOnly ? 'INVALID_RESPONSE' : 'WRITE_UNCERTAIN', 'REST response is not JSON; verify persistence before retrying a write'); }
    return {data, pages:res.headers.get('X-WP-TotalPages')};
  }
  route(registration) {
    const {rest_namespace:ns = 'wp/v2', rest_base:base} = registration;
    if (!/^[a-zA-Z0-9_-]+(?:\/[a-zA-Z0-9_-]+)*$/.test(ns) || !/^[a-zA-Z0-9_-]+$/.test(base ?? '')) throw new WpError('ROUTE_INVALID','Invalid discovered REST route');
    return `/wp-json/${ns}/${base}`;
  }
  async discover() {
    const article = (await this.request('/wp-json/wp/v2/types/ht_kb')).data;
    if (article.slug !== 'ht_kb') throw new WpError('TYPE_INVALID','Discovered type is not ht_kb');
    this.route(article);
    const all = (await this.request('/wp-json/wp/v2/taxonomies')).data;
    const candidates = Object.entries(all).filter(([key,t]) => article.taxonomies?.includes(key) && t.types?.includes('ht_kb') && t.hierarchical).map(([key,t])=>({key,...t}));
    for (const t of candidates) this.route(t);
    const selected = this.categoryTaxonomy ? candidates.find(t=>t.key===this.categoryTaxonomy) : candidates.length === 1 ? candidates[0] : null;
    if (this.categoryTaxonomy && !selected) throw new WpError('TAXONOMY_INVALID','Configured category taxonomy is not an associated hierarchical ht_kb taxonomy');
    const schema=(await this.request(this.route(article),{method:'OPTIONS'})).data?.schema;
    if(selected) {
      const field=selected.rest_base;
      if(schema?.properties?.[field]?.type!=='array' || schema.properties[field].readonly)throw new WpError('TAXONOMY_FIELD_INVALID','Category field not verified in article schema');
      selected.article_field=field;
    }
    return {article, category_candidates:candidates, category:selected, category_selection_required:!selected, schema};
  }
  async verifyConnection() {
    const result={...this.connectionStatus(),reachable:false,authenticated:false,edit_access:false,publish_access:'unverified'};
    try {
      const discovery=await this.discover(); result.reachable=true;
      result.article_rest_base=discovery.article.rest_base; result.category_selection_required=discovery.category_selection_required;
      if (result.credentials_present) {
        await this.request('/wp-json/wp/v2/users/me?context=edit&_fields=id'); result.authenticated=true;
        await this.request(`${this.route(discovery.article)}?context=edit&per_page=1`); result.edit_access=true;
      }
    } catch(e) { result.error_code=e instanceof WpError ? e.code : 'VERIFICATION_FAILED'; }
    return result;
  }
  requireCredentials() { if (!(this.username && this.password)) throw new WpError('AUTH_REQUIRED','Provision REST credentials outside the skill and repository'); }
  requireWrites() { if (!this.allowWrites) throw new WpError('WRITES_DISABLED','Writes disabled; enable PAWA_WP_ALLOW_WRITES only for authorized documentation work'); this.requireCredentials(); }
  async collect(path, params={}) {
    const items=[];
    for (let page=1;page<=20;page++) {
      const query=new URLSearchParams({...params,per_page:'100',page:String(page)});
      const {data,pages}=await this.request(`${path}?${query}`);
      if (!Array.isArray(data)) throw new WpError('INVALID_RESPONSE','REST collection is not an array');
      items.push(...data);
      const total=Number(pages);
      if (pages !== null && Number.isInteger(total) && total >= 0) {
        if(page>=total)return {items,complete:true};
      } else if(data.length<100)return {items,complete:true};
    }
    return {items,complete:false,limit:'20 pages'};
  }
  async categories() {
    const discovery=await this.discover();
    if(!discovery.category) throw new WpError('TAXONOMY_AMBIGUOUS','Choose PAWA_WP_CATEGORY_TAXONOMY from discovered associated categories');
    return {...await this.collect(this.route(discovery.category),{hide_empty:'false'}),taxonomy:discovery.category.key,article_field:discovery.category.article_field};
  }
  async search({search='',slug='',statuses=STATUSES}={}) {
    if (!Array.isArray(statuses) || !statuses.length || statuses.some(s=>!STATUSES.includes(s))) throw new WpError('STATUS_INVALID','Unsupported article statuses');
    const d=await this.discover(); const items=[]; const unavailable=[]; let complete=true;
    for (const status of statuses) {
      if(status!=='publish' && !(this.username && this.password)) {unavailable.push(status);complete=false;continue;}
      try {
        const result=await this.collect(this.route(d.article),{status,...(search?{search}:{}),...(slug?{slug}:{}),...(this.username&&this.password?{context:'edit'}:{})});
        items.push(...result.items.map(item=>this.articleFields(item,d))); complete &&=result.complete;
      } catch(e) { if (!(e instanceof WpError)) throw e; unavailable.push({status,error_code:e.code});complete=false; }
    }
    return {items,complete,unavailable_statuses:unavailable};
  }
  async read({id}) {
    this.requireCredentials(); this.validId(id);
    const d=await this.discover();
    const article=(await this.request(`${this.route(d.article)}/${id}?context=edit`)).data;
    if(article.type!=='ht_kb' || article.id!==id) throw new WpError('TYPE_INVALID','Read did not return the intended ht_kb article');
    return this.articleFields(article,d);
  }
  articleFields(article,discovery) {
    const allowed=['id','type','status','slug','title','content','excerpt','modified_gmt','date_gmt','link',...(discovery.category?[discovery.category.article_field]:[])];
    return Object.fromEntries(allowed.filter(key=>Object.hasOwn(article,key)).map(key=>[key,article[key]]));
  }
  validId(id) {if(!Number.isInteger(id)||id<=0)throw new WpError('ID_INVALID','Positive article ID required');}
  async prepareFields(fields,create=false) {
    const allowed=['title','content','slug','excerpt','categories'];
    if(Object.keys(fields).some(k=>!allowed.includes(k)))throw new WpError('FIELD_INVALID','Unsupported article field');
    if(create && allowed.some(k=>fields[k]===undefined))throw new WpError('FIELD_REQUIRED','Title, content, slug, excerpt and categories required');
    const body={};
    for(const key of ['title','content','slug','excerpt']) if(fields[key]!==undefined) {
      if(typeof fields[key]!=='string')throw new WpError('FIELD_INVALID','Article text fields must be strings'); body[key]=fields[key];
    }
    if(body.title!==undefined && !body.title.trim())throw new WpError('FIELD_INVALID','Title cannot be empty');
    if(body.slug!==undefined && !/^[a-z0-9]+(?:-[a-z0-9]+)*$/.test(body.slug))throw new WpError('FIELD_INVALID','Use a lowercase hyphenated slug');
    if(fields.categories!==undefined) {
      if(!Array.isArray(fields.categories)||!fields.categories.length||fields.categories.some(x=>!Number.isInteger(x)||x<=0))throw new WpError('FIELD_INVALID','Existing category IDs required');
      const terms=await this.categories();
      if(!terms.complete || fields.categories.some(id=>!terms.items.some(t=>t.id===id)))throw new WpError('CATEGORY_INVALID','Category IDs must exist in the verified ht_kb taxonomy');
      body[terms.article_field]=[...new Set(fields.categories)];
    }
    return body;
  }
  async verifySaved(id,body) {
    const article=await this.read({id}); const differences=[];
    for(const [key,value] of Object.entries(body)) {
      const actual=['title','content','excerpt'].includes(key)?article[key]?.raw:article[key];
      const expected=Array.isArray(value)?[...value].sort((a,b)=>a-b):value;
      const comparison=Array.isArray(actual)?[...actual].sort((a,b)=>a-b):actual;
      if(JSON.stringify(comparison)!==JSON.stringify(expected))differences.push(key);
    }
    return {article,verified:differences.length===0,differences,browser_verification:'required',concurrency:'client preflight only; not atomic'};
  }
  async writeAndVerify(route,body) {
    const saved=(await this.request(route,{method:'POST',body})).data;
    if(!saved || typeof saved!=='object' || Array.isArray(saved) || !Number.isInteger(saved.id)||saved.id<=0)throw new WpError('WRITE_UNCERTAIN','Write returned no usable article ID; reconcile before retrying');
    try {return await this.verifySaved(saved.id,body);}
    catch {throw new WpError('READBACK_FAILED',`Article ${saved.id} write returned success but read-back is unverified; do not repeat the write`);}
  }
  async createDraft(fields) {
    this.requireWrites(); const body=await this.prepareFields(fields,true); const d=await this.discover();
    return this.writeAndVerify(this.route(d.article),{...body,status:'draft'});
  }
  async checkVersion(id,expected) {
    if(typeof expected!=='string'||!expected)throw new WpError('VERSION_REQUIRED','expected_modified_gmt required');
    const current=await this.read({id});
    if(current.modified_gmt!==expected)throw new WpError('VERSION_CONFLICT','Article changed; reconcile before updating');
    return current;
  }
  async update({id,expected_modified_gmt,intent,...fields}) {
    this.requireWrites();
    if(!['draft','live_update'].includes(intent))throw new WpError('INTENT_REQUIRED','Explicit draft or live_update intent required');
    const body=await this.prepareFields(fields);
    if(!Object.keys(body).length)throw new WpError('FIELD_REQUIRED','At least one article field required');
    const d=await this.discover(); const current=await this.checkVersion(id,expected_modified_gmt);
    if(intent==='draft' && current.status!=='draft')throw new WpError('DRAFT_UNSUPPORTED','Cannot draft-edit a published article; save a separate local revision');
    return this.writeAndVerify(`${this.route(d.article)}/${id}`,{...body,status:current.status});
  }
  async publish({id,expected_modified_gmt,intent}) {
    this.requireWrites(); if(intent!=='publish')throw new WpError('INTENT_REQUIRED','Explicit publish intent required');
    const d=await this.discover(); const current=await this.checkVersion(id,expected_modified_gmt);
    if(current.status!=='draft')throw new WpError('STATUS_INVALID','Publish an inspected draft; live edits use update');
    return this.writeAndVerify(`${this.route(d.article)}/${id}`,{status:'publish'});
  }
}
