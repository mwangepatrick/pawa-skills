import test from 'node:test';
import assert from 'node:assert/strict';
import { definitions, callTool } from '../src/tools.mjs';
test('tools are limited to documentation; no arbitrary URL, type, credential, FTP, user or settings arguments',()=>{
  assert.equal(definitions.length,9);
  for(const tool of definitions) {
    assert.equal(tool.inputSchema.additionalProperties,false);
    assert.ok(!Object.keys(tool.inputSchema.properties).some(k=>['url','type','password','username','site','meta','status'].includes(k)));
  }
});
test('strict validation rejects unpublish/status and arbitrary credentials',async()=>{
  const result=await callTool({},'wp_update_article',{id:150,expected_modified_gmt:'date',intent:'draft',status:'draft'});
  assert.equal(result.isError,true); assert.match(result.content[0].text,/ARGS_INVALID/);
});
test('unexpected handler error never exposes secret details',async()=>{
  const result=await callTool({connectionStatus(){throw new Error('a-secret');}},'wp_connection_status',{});
  assert.equal(result.isError,true); assert.ok(!result.content[0].text.includes('a-secret'));
});
