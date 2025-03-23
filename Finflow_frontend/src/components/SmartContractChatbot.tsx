import React from 'react';

const SmartContractChatbot = () => {
  return (
    <div className="h-screen w-full flex items-center justify-center">
      <iframe 
        src="https://comforting-valkyrie-08ef54.netlify.app" 
        title="Smart Contract Assistant"
        className="w-full h-full border-none"
      />
    </div>
  );
};

export default SmartContractChatbot;