import React from 'react';
import { useNavigate } from 'react-router-dom';
import LoginForm from '@/components/auth/LoginForm';
import { ArrowLeft } from 'lucide-react';
import Logo from '../assets/logo.png';

const Login = () => {
  const navigate = useNavigate();
  
  return (
    <div className="min-h-screen bg-background flex flex-col">
      <div className="flex-1 flex flex-col justify-center items-center p-4 sm:p-8">
        <div className="w-full max-w-md">
          <button 
            onClick={() => navigate('/')}
            className="mb-8 inline-flex items-center text-sm font-medium text-muted-foreground hover:text-primary transition-colors"
          >
            <ArrowLeft className="mr-2 h-4 w-4" />
            Back to home
          </button>
          
          <div className="space-y-2 text-center mb-8">
            <img src={Logo} alt="FinFlow Logo" className="mx-auto h-12 w-12" />
            {/* <div className="mx-auto h-12 w-12 flex items-center justify-center rounded-lg bg-primary overflow-hidden mb-2">
              <span className="text-white font-semibold text-xl">FF</span>
            </div> */}
            <h1 className="text-2xl font-bold">Welcome back</h1>
            <p className="text-muted-foreground">Sign in to your FinFlow account</p>
          </div>
          
          <LoginForm />
        </div>
      </div>
      
      <footer className="py-6 border-t border-border">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 md:px-10">
          <div className="flex justify-center items-center">
            <div className="text-sm text-muted-foreground">
              © 2025 FinFlow. All rights reserved.
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default Login; 