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
import Link from 'next/link'

interface Message {
  time: string;
  message: string;
}

export function HomePage() {
  const [isRecording, setIsRecording] = useState(false)  
  const [messages, setMessages] = useState<Message[]>([]);
  const [environmentMessages, setEnvironmentMessages] = useState<string[]>([]);
  const [currentMessageIndex, setCurrentMessageIndex] = useState(0);

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

      <div className="max-w-5xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8">
        <section className="w-full space-y-8">
          <article className="relative">
            <div className="w-full aspect-video bg-muted rounded-lg flex items-center justify-center border-2 border-dashed border-muted-foreground">
              <CameraStream />
            </div>
          </article>

          <article className="w-full space-y-4">
            <header className="flex justify-between items-center">
              <h2 className="text-2xl font-semibold">Live Captions</h2>
              <div className="flex items-center gap-3 bg-white dark:bg-slate-700 px-4 py-2 rounded-full shadow-sm">
                <span className="text-sm font-medium">
                  Status: {isRecording ? 'Active' : 'Inactive'}
                </span>
                <div className={`w-3 h-3 rounded-full ${isRecording ? 'bg-green-500 animate-pulse' : 'bg-red-500'}`} />
              </div>
            </header>

            <div 
              className="h-[200px] w-full bg-muted rounded-lg p-4 overflow-y-auto space-y-2"
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
          </article>
        </section>

        <footer className="w-full flex flex-col gap-4 py-4">
          <div className="flex justify-center gap-4">
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
        </footer>
      </div>
    </main>
  );
}