interface MessageProcessorConfig {
  minLength: number;
  maxLength: number;
}

export function processMessages(
  rawMessages: { message: string }[],
  config: MessageProcessorConfig = { minLength: 40, maxLength: 80 }
): string[] {
  const splitMessages = rawMessages
    .map(item => item.message
      .split('.')
      .map(msg => msg.trim())
      .filter(msg => msg.length > 0)
    )
    .flat();

  const processedMessages: string[] = [];
  let currentMessage = '';

  for (const msg of splitMessages) {
    if (currentMessage) {
      const combined = currentMessage + '. ' + msg;
      if (combined.length <= config.maxLength) {
        currentMessage = combined;
      } else {
        if (currentMessage.length >= config.minLength) {
          processedMessages.push(currentMessage);
        }
        currentMessage = msg;
      }
    } else {
      currentMessage = msg;
    }
    if (currentMessage.length >= config.minLength && currentMessage.length <= config.maxLength) {
      processedMessages.push(currentMessage);
      currentMessage = '';
    }
  }

  if (currentMessage.length >= config.minLength && currentMessage.length <= config.maxLength) {
    processedMessages.push(currentMessage);
  }

  return processedMessages;
}