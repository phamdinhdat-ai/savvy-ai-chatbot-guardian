
import React from 'react';
import { cn } from '@/lib/utils';
import { Avatar } from '@/components/ui/avatar';
import { Bot, User } from 'lucide-react';

interface ChatMessageProps {
  message: string;
  isUser: boolean;
  timestamp: Date;
}

const ChatMessage: React.FC<ChatMessageProps> = ({ message, isUser, timestamp }) => {
  return (
    <div 
      className={cn(
        "flex w-full mb-4 animate-message-fade-in",
        isUser ? "justify-end" : "justify-start"
      )}
    >
      <div 
        className={cn(
          "flex max-w-[80%] md:max-w-[70%]",
          isUser ? "flex-row-reverse" : "flex-row",
        )}
      >
        <Avatar className={cn(
          "h-8 w-8 mt-1", 
          isUser ? "ml-2 bg-chatbot-secondary" : "mr-2 bg-chatbot-accent"
        )}>
          <div className="flex h-full items-center justify-center">
            {isUser ? <User className="h-5 w-5 text-white" /> : <Bot className="h-5 w-5 text-white" />}
          </div>
        </Avatar>
        
        <div>
          <div 
            className={cn(
              "rounded-lg px-4 py-2 text-sm",
              isUser 
                ? "bg-chatbot-secondary text-white rounded-tr-none" 
                : "bg-chatbot-light text-chatbot-primary rounded-tl-none"
            )}
          >
            {message}
          </div>
          <div 
            className={cn(
              "text-xs mt-1 text-gray-500",
              isUser ? "text-right" : "text-left"
            )}
          >
            {timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
          </div>
        </div>
      </div>
    </div>
  );
};

export default ChatMessage;
