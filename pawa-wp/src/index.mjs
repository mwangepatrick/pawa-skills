import { Server } from '@modelcontextprotocol/sdk/server/index.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import { CallToolRequestSchema, ListToolsRequestSchema } from '@modelcontextprotocol/sdk/types.js';
import { PawaWpClient } from './client.mjs';
import { definitions, callTool } from './tools.mjs';

const client=new PawaWpClient({
  username:process.env.PAWA_WP_USERNAME,
  password:process.env.PAWA_WP_APPLICATION_PASSWORD,
  allowWrites:process.env.PAWA_WP_ALLOW_WRITES==='true',
  categoryTaxonomy:process.env.PAWA_WP_CATEGORY_TAXONOMY,
});
const server=new Server({name:'pawa-wp',version:'0.1.0'},{capabilities:{tools:{}}});
server.setRequestHandler(ListToolsRequestSchema,async()=>({tools:definitions.map(({method,...definition})=>definition)}));
server.setRequestHandler(CallToolRequestSchema,async({params})=>callTool(client,params.name,params.arguments??{}));
await server.connect(new StdioServerTransport());
