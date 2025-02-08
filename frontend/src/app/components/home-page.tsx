"use client";

import { Button } from "@/components/ui/button";
import { useState } from "react";

export function HomePage() {
  const [isRecording, setIsRecording] = useState(false);

  return (
    <main className="flex flex-col items-center space-y-8 w-full max-w-5xl mx-auto">
      <header className="space-y-4 text-center w-full">
        <h1 className="text-4xl font-bold sm:text-5xl">
          iAssist
        </h1>
        <p className="text-muted-foreground text-lg">
          Computer vision assistance for the visually impaired
        </p>
      </header>

      <section className="w-full space-y-8">
        <article className="relative">
          <div className="w-full aspect-video bg-muted rounded-lg flex items-center justify-center border-2 border-dashed border-muted-foreground">
            <p className="text-muted-foreground" role="status" aria-live="polite">
              Camera feed will appear here
            </p>
          </div>

          <div className="absolute bottom-4 right-4 flex gap-2">
            <Button 
              size="sm" 
              variant="secondary"
              title="Toggle fullscreen"
              aria-label="Toggle fullscreen view"
            >
              <span className="sr-only">Fullscreen</span>
              □
            </Button>
          </div>
        </article>

        <article className="w-full space-y-4">
          <header className="flex justify-between items-center">
            <h2 className="text-2xl font-semibold">Live Captions</h2>
            <div className="flex items-center gap-2">
              <span className="text-sm text-muted-foreground">
                Status: {isRecording ? 'Active' : 'Inactive'}
              </span>
              <div className={`w-3 h-3 rounded-full ${isRecording ? 'bg-green-500' : 'bg-red-500'}`} />
            </div>
          </header>

          <div 
            className="h-[200px] w-full bg-muted rounded-lg p-4 overflow-y-auto space-y-2"
            role="log"
            aria-live="polite"
            aria-label="Detection captions"
            style={{ scrollBehavior: 'smooth' }}
          >
            {[
              {
                time: "12:01 PM",
                message: "Warning: Stairs ahead, approximately 5 steps down. Handrail available on the right side."
              },
              {
                time: "12:00 PM",
                message: "Door detected 3 meters ahead. Push handle on the left side. The door opens outward."
              },
              {
                time: "11:59 AM",
                message: "Person approaching from the right, approximately 2 meters away. They appear to be waiting to pass."
              },
              {
                time: "11:58 AM",
                message: "Clear pathway ahead. Corridor width is approximately 2 meters. Wall guidance available on both sides."
              },
              {
                time: "11:57 AM",
                message: "Crosswalk signal is green. No vehicles detected. Safe to cross the street."
              },
              {
                time: "11:56 AM",
                message: "Restaurant entrance on the left. Automatic sliding doors. No steps detected."
              },
              {
                time: "11:55 AM",
                message: "Bench detected 1 meter to your right. Approximately 1.5 meters long."
              },
              {
                time: "11:54 AM",
                message: "Elevator buttons: Ground floor highlighted. Up and down arrows available."
              },
              {
                time: "11:53 AM",
                message: "Wide open space ahead. Indoor lobby area. Multiple seating areas detected."
              },
              {
                time: "11:52 AM",
                message: "Information desk 5 meters ahead. Staff member present."
              }
            ].map((caption, index) => (
              <div 
                key={index} 
                className="flex items-start gap-2 p-2 rounded hover:bg-muted-foreground/5 transition-colors"
              >
                <time className="text-sm text-muted-foreground whitespace-nowrap" dateTime={caption.time}>
                  {caption.time}:
                </time>
                <p className="text-foreground">{caption.message}</p>
              </div>
            ))}
          </div>
        </article>
      </section>

      <footer className="w-full flex flex-col gap-4">
        <div className="flex justify-center gap-4">
          <Button 
            size="lg" 
            variant={isRecording ? "destructive" : "default"}
            onClick={() => setIsRecording(!isRecording)}
            aria-pressed={isRecording}
          >
            {isRecording ? "Stop Detection" : "Start Detection"}
          </Button>
        </div>
      </footer>
    </main>
  );
}