export interface ChatbotResponse {
  answer: string;
}

export interface Message {
  type: 'user' | 'bot';
  content: string;
}