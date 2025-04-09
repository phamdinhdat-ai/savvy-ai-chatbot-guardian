
import React from 'react';
import ChatInterface from '@/components/ChatInterface';
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";

const Index = () => {
  return (
    <div className="min-h-screen bg-gradient-to-b from-gray-50 to-gray-100 flex flex-col">
      <header className="bg-white shadow-sm py-4 px-6">
        <div className="max-w-7xl mx-auto flex justify-between items-center">
          <div className="flex items-center">
            <span className="text-2xl font-bold bg-gradient-to-r from-chatbot-primary to-chatbot-accent bg-clip-text text-transparent">
              SavvyAI Guardian
            </span>
          </div>
          <nav>
            <ul className="flex space-x-6">
              <li>
                <a href="#features" className="text-gray-600 hover:text-chatbot-accent transition-colors">
                  Features
                </a>
              </li>
              <li>
                <a href="#deployment" className="text-gray-600 hover:text-chatbot-accent transition-colors">
                  Deployment
                </a>
              </li>
              <li>
                <a href="#about" className="text-gray-600 hover:text-chatbot-accent transition-colors">
                  About
                </a>
              </li>
            </ul>
          </nav>
        </div>
      </header>

      <main className="flex-1 p-6">
        <div className="max-w-7xl mx-auto">
          <div className="text-center mb-10">
            <h1 className="text-4xl font-bold text-chatbot-primary mb-4">
              Advanced AI Chatbot with RAG & Guardrails
            </h1>
            <p className="text-gray-600 max-w-2xl mx-auto">
              A powerful, secure AI assistant built with Python, deployed on Kubernetes,
              and enhanced with Retrieval Augmented Generation and safety Guardrails.
            </p>
          </div>

          <Tabs defaultValue="chatbot" className="max-w-4xl mx-auto">
            <TabsList className="grid grid-cols-2 mb-8">
              <TabsTrigger value="chatbot">Interactive Demo</TabsTrigger>
              <TabsTrigger value="technology">Technology Stack</TabsTrigger>
            </TabsList>
            
            <TabsContent value="chatbot" className="flex justify-center">
              <ChatInterface />
            </TabsContent>
            
            <TabsContent value="technology">
              <div className="grid md:grid-cols-2 gap-6">
                <div className="bg-white p-6 rounded-lg shadow-md">
                  <h3 className="text-lg font-semibold text-chatbot-primary mb-3">
                    AI & Machine Learning
                  </h3>
                  <ul className="space-y-2 text-gray-700">
                    <li className="flex items-start">
                      <span className="text-chatbot-accent font-bold mr-2">•</span>
                      <span><strong>RAG:</strong> Retrieval Augmented Generation for knowledge-enhanced responses</span>
                    </li>
                    <li className="flex items-start">
                      <span className="text-chatbot-accent font-bold mr-2">•</span>
                      <span><strong>Guardrails:</strong> Safety mechanisms to ensure appropriate AI behavior</span>
                    </li>
                    <li className="flex items-start">
                      <span className="text-chatbot-accent font-bold mr-2">•</span>
                      <span><strong>LLMs:</strong> Advanced language models for natural conversation</span>
                    </li>
                    <li className="flex items-start">
                      <span className="text-chatbot-accent font-bold mr-2">•</span>
                      <span><strong>Vector Database:</strong> For efficient semantic search and retrieval</span>
                    </li>
                  </ul>
                </div>
                
                <div className="bg-white p-6 rounded-lg shadow-md">
                  <h3 className="text-lg font-semibold text-chatbot-primary mb-3">
                    Infrastructure & Deployment
                  </h3>
                  <ul className="space-y-2 text-gray-700">
                    <li className="flex items-start">
                      <span className="text-chatbot-accent font-bold mr-2">•</span>
                      <span><strong>Python:</strong> Core language for AI/ML implementation</span>
                    </li>
                    <li className="flex items-start">
                      <span className="text-chatbot-accent font-bold mr-2">•</span>
                      <span><strong>Docker:</strong> Containerization for consistent environments</span>
                    </li>
                    <li className="flex items-start">
                      <span className="text-chatbot-accent font-bold mr-2">•</span>
                      <span><strong>Kubernetes:</strong> Orchestration for scalable deployment</span>
                    </li>
                    <li className="flex items-start">
                      <span className="text-chatbot-accent font-bold mr-2">•</span>
                      <span><strong>API Gateway:</strong> For secure external communications</span>
                    </li>
                  </ul>
                </div>
              </div>
            </TabsContent>
          </Tabs>
        </div>
      </main>

      <footer className="bg-chatbot-dark text-white py-6 mt-12">
        <div className="max-w-7xl mx-auto px-6 text-center">
          <p>SavvyAI Guardian: Advanced AI Chatbot with RAG & Guardrails</p>
          <p className="text-sm text-gray-400 mt-2">
            © {new Date().getFullYear()} - Kubernetes-ready AI Application
          </p>
        </div>
      </footer>
    </div>
  );
};

export default Index;
