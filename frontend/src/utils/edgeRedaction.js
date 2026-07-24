import { pipeline } from '@xenova/transformers';

let nerPipeline = null;

export const initEdgeModel = async () => {
  if (!nerPipeline) {
    nerPipeline = await pipeline('token-classification', 'Xenova/bert-base-NER');
  }
  return nerPipeline;
};

export const redactTextAtEdge = async (text) => {
  if (!text) return text;
  
  const pipe = await initEdgeModel();
  const entities = await pipe(text);
  
  let redactedText = text;
  
  const sortedEntities = [...entities].sort((a, b) => b.start - a.start);
  
  for (const entity of sortedEntities) {
    if (['PER', 'ORG', 'LOC'].includes(entity.entity_group)) {
      redactedText = 
        redactedText.substring(0, entity.start) + 
        `[${entity.entity_group}]` + 
        redactedText.substring(entity.end);
    }
  }
  
  return redactedText;
};
