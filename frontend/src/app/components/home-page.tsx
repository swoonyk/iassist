"use client";

import { Button } from "@/components/ui/button";
import { useState, useEffect } from "react";
import { processMessages } from "../lib/message-cutter";
import { AnimatedText } from "@/components/ui/animated-underline-text-one";
const CameraStream = dynamic(() => import('./CameraStream').then(mod => mod.CameraStream), {
  ssr: false,
  loading: () => <p>Loading camera...</p>
})
import dynamic from 'next/dynamic'

interface Message {
  time: string;
  message: string;
}

export function HomePage() {
  const [isRecording, setIsRecording] = useState(false)  
  const [messages, setMessages] = useState<Message[]>([]);
  const [environmentMessages, setEnvironmentMessages] = useState<string[]>([]);
  const [currentMessageIndex, setCurrentMessageIndex] = useState(0);
  const [isCameraStarted, setIsCameraStarted] = useState(false);

  useEffect(() => {
    fetch('http://localhost:5003/api/environment-messages')
      .then(response => {
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        return response.json();
      })
      .then(data => {
        setEnvironmentMessages(data.messages);
      })
      .catch(error => {
        console.error('Error fetching environment messages:', error);
        setEnvironmentMessages([]);
      });
  }, []);

  const addMessage = (newMessage: Message) => {
    if (isRecording) {
      setMessages(prevMessages => [newMessage, ...prevMessages]);
    }
  };

  const handleNewData = (jsonData: string) => {
    try {
      const data = JSON.parse(jsonData);
      if (data.time && data.message) {
        addMessage({
          time: data.time,
          message: data.message
        });
      }
    } catch (error) {
      console.error('Error parsing JSON:', error);
    }
  };

  useEffect(() => {
    let interval: NodeJS.Timeout;
    
    if (isRecording && environmentMessages.length > 0) {
      interval = setInterval(() => {
        const message = environmentMessages[currentMessageIndex];
        
        const testJson = JSON.stringify({
          time: new Date().toLocaleTimeString(),
          message: message
        });
        handleNewData(testJson);
        
        setCurrentMessageIndex(prevIndex => 
          prevIndex + 1 >= environmentMessages.length ? 0 : prevIndex + 1
        );
      }, 3000); 
    }

    return () => {
      if (interval) {
        clearInterval(interval);
      }
    };
  }, [isRecording, environmentMessages, currentMessageIndex]);

  const handleStartClick = () => {
    setIsRecording(true);
  };

  return (
    <main className="flex flex-col items-center w-full">
      <div className="w-full bg-gradient-to-b from-white to-slate-50 dark:from-zinc-900 dark:to-zinc-950 py-16">
        <header className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 space-y-6 text-center">
          <AnimatedText 
            text="iAssist"
            textClassName="text-5xl font-extrabold bg-gradient-to-r from-blue-500 via-blue-600 to-indigo-600 bg-clip-text text-transparent"
            underlineClassName="text-blue-500 dark:text-blue-400"
          />
          <h3 className="text-xl text-slate-600 dark:text-slate-300 max-w-2xl mx-auto">
            Computer vision assistance for the visually impaired
          </h3>
        </header>
      </div>

      <div className="max-w-5xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-12">
        {/* Camera Box */}
        <div className="w-full p-8 bg-white/50 dark:bg-zinc-900/50 backdrop-blur-sm rounded-xl shadow-xl border border-slate-200 dark:border-slate-800">
          <div className="flex items-center gap-3 mb-6">
            <div className="p-2 bg-blue-100 dark:bg-blue-900/50 rounded-lg">
              <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="text-blue-500"><path d="M14.5 4h-5L7 7H4a2 2 0 0 0-2 2v9a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2V9a2 2 0 0 0-2-2h-3l-2.5-3z"></path><circle cx="12" cy="13" r="3"></circle></svg>
            </div>
            <h2 className="text-2xl font-bold text-slate-800 dark:text-slate-100">Live Camera</h2>
          </div>
          <div className="w-full aspect-video bg-muted rounded-lg flex items-center justify-center border-2 border-dashed border-muted-foreground overflow-hidden">
            {isCameraStarted ? (
              <CameraStream />
            ) : (
              <div className="flex flex-col items-center gap-4">
                <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="text-slate-400"><path d="M14.5 4h-5L7 7H4a2 2 0 0 0-2 2v9a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2V9a2 2 0 0 0-2-2h-3l-2.5-3z"></path><circle cx="12" cy="13" r="3"></circle></svg>
                <Button 
                  onClick={() => setIsCameraStarted(true)}
                  size="lg"
                  className="bg-gradient-to-r from-blue-500 to-indigo-600 hover:from-blue-600 hover:to-indigo-700 text-white shadow-lg"
                >
                  Start Camera
                </Button>
              </div>
            )}
          </div>
        </div>

        {/* Live Actions Box
        <div className="w-full p-8 bg-white/50 dark:bg-zinc-900/50 backdrop-blur-sm rounded-xl shadow-xl border border-slate-200 dark:border-slate-800">
          <div className="flex justify-between items-center mb-6">
            <div className="flex items-center gap-3">
              <div className="p-2 bg-blue-100 dark:bg-blue-900/50 rounded-lg">
                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="text-blue-500"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path></svg>
              </div>
              <h2 className="text-2xl font-bold text-slate-800 dark:text-slate-100">Live Actions</h2>
            </div>
            <div className="flex items-center gap-3 bg-white dark:bg-slate-700 px-4 py-2 rounded-full shadow-sm">
              <span className="text-sm font-medium">
                Status: {isRecording ? 'Active' : 'Inactive'}
              </span>
              <div className={`w-3 h-3 rounded-full ${isRecording ? 'bg-green-500 animate-pulse' : 'bg-red-500'}`} />
            </div>
          </div>

          <div className="space-y-6">
            <div 
              className="h-[300px] w-full bg-muted rounded-lg p-4 overflow-y-auto space-y-2 border border-slate-200 dark:border-slate-700"
              role="log"
              aria-live="polite"
              aria-label="Detection captions"
              style={{ scrollBehavior: 'smooth' }}
            >
              {messages.map((caption, index) => (
                <div 
                  key={index} 
                  className="flex items-start gap-3 p-3 rounded-lg bg-slate-50 dark:bg-slate-800 hover:bg-slate-100 dark:hover:bg-slate-700 transition-colors"
                >
                  <time 
                    className="text-sm font-medium text-slate-500 dark:text-slate-400 whitespace-nowrap" 
                    dateTime={caption.time}
                  >
                    {caption.time}
                  </time>
                  <p className="text-slate-700 dark:text-slate-200">{caption.message}</p>
                </div>
              ))}
            </div>

            <div className="flex justify-center pt-4">
              <Button 
                size="lg" 
                variant={isRecording ? "destructive" : "default"}
                onClick={() => setIsRecording(!isRecording)}
                aria-pressed={isRecording}
                className="px-8 py-6 text-lg font-semibold shadow-lg hover:shadow-xl transition-all"
              >
                {isRecording ? "Stop Detection" : "Start Detection"}
              </Button>
            </div>
          </div>
        </div> */}
      </div>
    </main>
  );
}