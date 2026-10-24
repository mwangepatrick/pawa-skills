import { WpError } from './client.mjs';

const text = {type:'string'};
const id = {type:'integer',minimum:1};
const fields = {title:text,content:text,slug:text,excerpt:text,categories:{type:'array',minItems:1,items:id}};
const tool = (name,description,method,properties={},required=[],readOnly=true) => ({
  name,description,method,inputSchema:{type:'object',properties,required,additionalProperties:false},
  annotations:{readOnlyHint:readOnly,destructiveHint:!readOnly,idempotentHint:readOnly,openWorldHint:true},
});
export const definitions = [
  tool('wp_connection_status','Report fixed PawaPos docs target and credential presence; never returns secrets','connectionStatus'),
  tool('wp_verify_connection','Read-only REST and authenticated edit-access checks; publish permission remains unverified','verifyConnection'),
  tool('wp_discover_articles','Discover ht_kb registration and associated category REST routes','discover'),
  tool('wp_list_categories','List existing PawaPos article categories with pagination completeness','categories'),
  tool('wp_search_articles','Search ht_kb articles across requested statuses; inspect completeness before creating','search',{search:text,slug:text,statuses:{type:'array',minItems:1,items:{type:'string',enum:['publish','draft','pending','private']}}}),
  tool('wp_read_article','Read raw ht_kb article in authenticated edit context','read',{id},['id']),
  tool('wp_create_draft','Create an authorized documentation draft; explicit fields, category validation and read-back; reconcile ambiguous writes','createDraft',fields,Object.keys(fields),false),
  tool('wp_update_article','Update authorized documentation fields with revision preflight; rejects draft-only edits of published articles','update',{id,expected_modified_gmt:text,intent:{type:'string',enum:['draft','live_update']},...fields},['id','expected_modified_gmt','intent'],false),
  tool('wp_publish_article','Publish an inspected draft only when requested; requires explicit intent, revision marker and browser verification','publish',{id,expected_modified_gmt:text,intent:{type:'string',enum:['publish']}},['id','expected_modified_gmt','intent'],false),
];
function validate(schema,value) {
  if(!value || typeof value!=='object' || Array.isArray(value))throw new WpError('ARGS_INVALID','Object arguments required');
  if(Object.keys(value).some(key=>!Object.hasOwn(schema.properties,key)))throw new WpError('ARGS_INVALID','Unknown argument');
  for(const key of schema.required) if(value[key]===undefined)throw new WpError('ARGS_INVALID',`Missing argument: ${key}`);
  for(const [key,v] of Object.entries(value)) {
    const s=schema.properties[key];
    if(s.type==='string' && typeof v!=='string' || s.type==='integer' && (!Number.isInteger(v)||v<s.minimum) || s.type==='array' && (!Array.isArray(v)||v.length<(s.minItems??0)))throw new WpError('ARGS_INVALID',`Invalid argument: ${key}`);
    if(s.enum && !s.enum.includes(v))throw new WpError('ARGS_INVALID',`Invalid argument: ${key}`);
    if(s.type==='array' && v.some(item=>s.items.type==='integer'? !Number.isInteger(item)||item<s.items.minimum:typeof item!=='string'||!s.items.enum.includes(item)))throw new WpError('ARGS_INVALID',`Invalid array: ${key}`);
  }
}
export async function callTool(client,name,args={}) {
  try {
    const definition=definitions.find(t=>t.name===name);
    if(!definition)throw new WpError('TOOL_UNKNOWN','Unknown documentation tool');
    validate(definition.inputSchema,args);
    const result=await client[definition.method](args);
    return {content:[{type:'text',text:JSON.stringify(result)}]};
  } catch(e) {
    const result=e instanceof WpError? {error:e.code,message:e.message}:{error:'INTERNAL_ERROR',message:'Documentation operation failed; sensitive details omitted'};
    return {isError:true,content:[{type:'text',text:JSON.stringify(result)}]};
  }
}
