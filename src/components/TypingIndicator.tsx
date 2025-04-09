
import React from 'react';

const TypingIndicator: React.FC = () => {
  return (
    <div className="flex items-center space-x-1 p-2 rounded-md bg-chatbot-light inline-block">
      <div className="w-2 h-2 rounded-full bg-chatbot-accent animate-pulse-light"></div>
      <div className="w-2 h-2 rounded-full bg-chatbot-accent animate-pulse-light" style={{ animationDelay: '0.2s' }}></div>
      <div className="w-2 h-2 rounded-full bg-chatbot-accent animate-pulse-light" style={{ animationDelay: '0.4s' }}></div>
    </div>
  );
};

export default TypingIndicator;
