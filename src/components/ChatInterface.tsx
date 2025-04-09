
import React, { useState, useRef, useEffect } from 'react';
import ChatMessage from './ChatMessage';
import ChatInput from './ChatInput';
import TypingIndicator from './TypingIndicator';
import { Card, CardContent, CardFooter, CardHeader, CardTitle } from '@/components/ui/card';

interface Message {
  id: string;
  content: string;
  isUser: boolean;
  timestamp: Date;
}

const ChatInterface: React.FC = () => {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: '1',
      content: "Hello! I'm your AI assistant powered by RAG (Retrieval Augmented Generation) and protected by Guardrails. How can I help you today?",
      isUser: false,
      timestamp: new Date()
    }
  ]);
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const handleSendMessage = async (content: string) => {
    // Add user message
    const userMessage: Message = {
      id: Date.now().toString(),
      content,
      isUser: true,
      timestamp: new Date()
    };
    
    setMessages(prevMessages => [...prevMessages, userMessage]);
    setIsLoading(true);
    
    // Simulate AI response with a delay
    try {
      // This would be replaced with actual API call to your Python backend
      setTimeout(() => {
        const aiMessage: Message = {
          id: (Date.now() + 1).toString(),
          content: generateMockResponse(content),
          isUser: false,
          timestamp: new Date()
        };
        setMessages(prevMessages => [...prevMessages, aiMessage]);
        setIsLoading(false);
      }, 1000);
    } catch (error) {
      console.error("Error getting AI response:", error);
      setIsLoading(false);
      // Add error message
      setMessages(prevMessages => [
        ...prevMessages, 
        {
          id: (Date.now() + 1).toString(),
          content: "Sorry, I encountered an error processing your request. Please try again.",
          isUser: false,
          timestamp: new Date()
        }
      ]);
    }
  };

  // Mock response function - this would be replaced by your actual Python backend call
  const generateMockResponse = (userMessage: string): string => {
    const lowerCaseMessage = userMessage.toLowerCase();
    
    if (lowerCaseMessage.includes("rag")) {
      return "RAG (Retrieval Augmented Generation) enhances AI responses by retrieving relevant information before generating answers. This helps provide more accurate and contextually relevant responses.";
    } else if (lowerCaseMessage.includes("guardrails")) {
      return "Guardrails are safety mechanisms that help ensure AI responses are safe, helpful, and aligned with human values. They can prevent harmful, biased, or irrelevant outputs.";
    } else if (lowerCaseMessage.includes("kubernetes") || lowerCaseMessage.includes("k8s")) {
      return "Kubernetes is an open-source container orchestration platform that automates deployment, scaling, and management of containerized applications. It's ideal for deploying AI systems at scale.";
    } else if (lowerCaseMessage.includes("docker") || lowerCaseMessage.includes("dockerfile")) {
      return "Docker is a platform for developing, shipping, and running applications in containers. A Dockerfile contains instructions for building a Docker image, which can then be deployed to Kubernetes.";
    } else if (lowerCaseMessage.includes("python")) {
      return "Python is a popular programming language for AI and machine learning due to its simplicity and extensive libraries. Frameworks like TensorFlow, PyTorch, and Hugging Face make it ideal for building sophisticated AI applications.";
    } else {
      return "I understand your query about " + userMessage.substring(0, 30) + "... In a full implementation, I would use RAG to retrieve relevant information and then generate a comprehensive response while ensuring it adheres to safety guidelines using Guardrails.";
    }
  };

  return (
    <Card className="w-full max-w-4xl h-[600px] flex flex-col shadow-lg border-chatbot-primary/20">
      <CardHeader className="bg-gradient-to-r from-chatbot-primary to-chatbot-secondary py-4">
        <CardTitle className="text-white flex items-center justify-center">
          AI Assistant with RAG & Guardrails
        </CardTitle>
      </CardHeader>
      
      <CardContent className="flex-1 overflow-y-auto p-4">
        <div className="space-y-4">
          {messages.map((msg) => (
            <ChatMessage 
              key={msg.id} 
              message={msg.content} 
              isUser={msg.isUser} 
              timestamp={msg.timestamp} 
            />
          ))}
          {isLoading && (
            <div className="flex justify-start mb-4">
              <TypingIndicator />
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>
      </CardContent>
      
      <CardFooter className="p-4 border-t border-gray-200">
        <ChatInput onSendMessage={handleSendMessage} isLoading={isLoading} />
      </CardFooter>
    </Card>
  );
};

export default ChatInterface;
