import React from 'react';
import { MessageSquare, Bot } from 'lucide-react';
import type { Message } from '../types';

interface ChatMessageProps {
  message: Message;
}

export function ChatMessage({ message }: ChatMessageProps) {
  const isBot = message.type === 'bot';
  
  return (
    <div className={`flex gap-3 ${isBot ? 'bg-gray-50' : ''} p-4 rounded-lg`}>
      <div className={`w-8 h-8 rounded-full flex items-center justify-center ${isBot ? 'bg-blue-100' : 'bg-gray-100'}`}>
        {isBot ? <Bot size={20} className="text-blue-600" /> : <MessageSquare size={20} className="text-gray-600" />}
      </div>
      <div className="flex-1">
        {message.content}
      </div>
    </div>
  );
}