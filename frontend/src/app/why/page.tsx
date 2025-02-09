"use client";

import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import {AnimatedText} from "@/components/ui/animated-underline-text-one";
export default function WhyPage() {
  return (
    <div className="min-h-screen bg-gradient-to-b from-white to-slate-50 dark:from-zinc-900 dark:to-zinc-950">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16 space-y-16">
        {/* Statistics Section */}
        <div className="space-y-8">
          <div className="text-center space-y-4">
            <AnimatedText 
                text="Why iAssist?"
                textClassName="text-5xl font-extrabold bg-gradient-to-r from-blue-500 via-blue-600 to-indigo-600 bg-clip-text text-transparent"
                underlineClassName="text-blue-500 dark:text-blue-400"
          />
            <p className="text-lg text-slate-600 dark:text-slate-400 max-w-2xl mx-auto">
              Empowering visually impaired individuals with cutting-edge AI technology for enhanced independence and accessibility.
            </p>
          </div>

          <Card className="border-0 shadow-xl bg-white/50 dark:bg-zinc-900/50 backdrop-blur-sm">
            <CardHeader>
              <CardTitle className="text-2xl font-bold text-slate-800 dark:text-slate-100">
                Understanding the Global Impact:
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-8">
              <div className="grid sm:grid-cols-2 gap-6">
                <div className="bg-blue-50 dark:bg-blue-950/50 rounded-lg p-6 border border-blue-100 dark:border-blue-900">
                  <p className="text-4xl font-bold text-blue-600 dark:text-blue-400">2.2 Billion</p>
                  <p className="text-sm text-blue-700 dark:text-blue-300 mt-2">People affected worldwide</p>
                </div>
                <div className="bg-indigo-50 dark:bg-indigo-950/50 rounded-lg p-6 border border-indigo-100 dark:border-indigo-900">
                  <p className="text-4xl font-bold text-indigo-600 dark:text-indigo-400">28%</p>
                  <p className="text-sm text-indigo-700 dark:text-indigo-300 mt-2">Of global population</p>
                </div>
              </div>
              <div className="space-y-4">
                <p className="text-slate-600 dark:text-slate-300 leading-relaxed">
                  Visual impairment represents one of the most significant health challenges we face today. These numbers underscore the critical importance of developing accessible technologies and solutions.
                </p>
                <p className="text-slate-600 dark:text-slate-300 leading-relaxed">
                  iAssist bridges this accessibility gap by leveraging cutting-edge AI technology to provide real-time assistance, making the world more navigable and accessible for people with visual impairments.
                </p>
              </div>
            </CardContent>
          </Card>
        </div>

        {/* SPECS Goals */}
        <div className="space-y-8">
          <div className="text-center space-y-4 max-w-3xl mx-auto">
            <h2 className="text-4xl font-bold text-slate-800 dark:text-slate-100">
              UN SPECS Goals
            </h2>
            <p className="text-lg text-slate-600 dark:text-slate-400">
              A comprehensive framework for addressing visual impairment challenges globally
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-5 gap-6">
            {/* Services */}
            <div className="group relative isolate">
              <div className="absolute inset-0 bg-blue-500 dark:bg-blue-600 rounded-2xl blur-xl opacity-20 transition-opacity duration-300 group-hover:opacity-30"></div>
              <div className="relative bg-gradient-to-br from-indigo-900 to-blue-900 p-6 rounded-2xl flex flex-col items-center text-center space-y-6 shadow-lg hover:shadow-xl transition-all duration-300 h-full">
                <div className="w-14 h-14 text-blue-300 transform group-hover:scale-110 transition-transform duration-300">
                  <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor">
                    <path d="M12 3c-4.97 0-9 4.03-9 9s4.03 9 9 9 9-4.03 9-9-4.03-9-9-9zm0 16c-3.87 0-7-3.13-7-7s3.13-7 7-7 7 3.13 7 7-3.13 7-7 7zm-.5-4.5c-.83 0-1.5-.67-1.5-1.5s.67-1.5 1.5-1.5 1.5.67 1.5 1.5-.67 1.5-1.5 1.5z"/>
                  </svg>
                </div>
                <h3 className="text-lg font-bold text-white">Improve access to refractive <span className="text-blue-300">Services</span></h3>
              </div>
            </div>

            {/* Personnel */}
            <div className="group relative isolate">
              <div className="absolute inset-0 bg-blue-500 dark:bg-blue-600 rounded-2xl blur-xl opacity-20 transition-opacity duration-300 group-hover:opacity-30"></div>
              <div className="relative bg-gradient-to-br from-indigo-900 to-blue-900 p-6 rounded-2xl flex flex-col items-center text-center space-y-6 shadow-lg hover:shadow-xl transition-all duration-300 h-full">
                <div className="w-14 h-14 text-blue-300 transform group-hover:scale-110 transition-transform duration-300">
                  <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor">
                    <path d="M16 11c1.66 0 2.99-1.34 2.99-3S17.66 5 16 5s-3 1.34-3 3 1.34 3 3 3zm-8 0c1.66 0 2.99-1.34 2.99-3S9.66 5 8 5 5 6.34 5 8s1.34 3 3 3zm0 2c-2.33 0-7 1.17-7 3.5V19h14v-2.5c0-2.33-4.67-3.5-7-3.5z"/>
                  </svg>
                </div>
                <h3 className="text-lg font-bold text-white">Build capacity of <span className="text-blue-300">Personnel</span></h3>
              </div>
            </div>

            {/* Education */}
            <div className="group relative isolate">
              <div className="absolute inset-0 bg-blue-500 dark:bg-blue-600 rounded-2xl blur-xl opacity-20 transition-opacity duration-300 group-hover:opacity-30"></div>
              <div className="relative bg-gradient-to-br from-indigo-900 to-blue-900 p-6 rounded-2xl flex flex-col items-center text-center space-y-6 shadow-lg hover:shadow-xl transition-all duration-300 h-full">
                <div className="w-14 h-14 text-blue-300 transform group-hover:scale-110 transition-transform duration-300">
                  <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor">
                    <path d="M21 17v-6.9L12 15 1 9l11-6 11 6v8h-2zm-9 4l-7-3.8v-8.37L12 13l7-3.8v8.37L12 21z"/>
                  </svg>
                </div>
                <h3 className="text-lg font-bold text-white">Improve population <span className="text-blue-300">Education</span></h3>
              </div>
            </div>

            {/* Cost */}
            <div className="group relative isolate">
              <div className="absolute inset-0 bg-blue-500 dark:bg-blue-600 rounded-2xl blur-xl opacity-20 transition-opacity duration-300 group-hover:opacity-30"></div>
              <div className="relative bg-gradient-to-br from-indigo-900 to-blue-900 p-6 rounded-2xl flex flex-col items-center text-center space-y-6 shadow-lg hover:shadow-xl transition-all duration-300 h-full">
                <div className="w-14 h-14 text-blue-300 transform group-hover:scale-110 transition-transform duration-300">
                  <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor">
                    <path d="M11.8 10.9c-2.27-.59-3-1.2-3-2.15 0-1.09 1.01-1.85 2.7-1.85 1.78 0 2.44.85 2.5 2.1h2.21c-.07-1.72-1.12-3.3-3.21-3.81V3h-3v2.16c-1.94.42-3.5 1.68-3.5 3.61 0 2.31 1.91 3.46 4.7 4.13 2.5.6 3 1.48 3 2.41 0 .69-.49 1.79-2.7 1.79-2.06 0-2.87-.92-2.98-2.1h-2.2c.12 2.19 1.76 3.42 3.68 3.83V21h3v-2.15c1.95-.37 3.5-1.5 3.5-3.55 0-2.84-2.43-3.81-4.7-4.4z"/>
                  </svg>
                </div>
                <h3 className="text-lg font-bold text-white">Reduce the <span className="text-blue-300">Cost</span></h3>
              </div>
            </div>

            {/* Surveillance */}
            <div className="group relative isolate">
              <div className="absolute inset-0 bg-blue-500 dark:bg-blue-600 rounded-2xl blur-xl opacity-20 transition-opacity duration-300 group-hover:opacity-30"></div>
              <div className="relative bg-gradient-to-br from-indigo-900 to-blue-900 p-6 rounded-2xl flex flex-col items-center text-center space-y-6 shadow-lg hover:shadow-xl transition-all duration-300 h-full">
                <div className="w-14 h-14 text-blue-300 transform group-hover:scale-110 transition-transform duration-300">
                  <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor">
                    <path d="M15.5 14h-.79l-.28-.27C15.41 12.59 16 11.11 16 9.5 16 5.91 13.09 3 9.5 3S3 5.91 3 9.5 5.91 16 9.5 16c1.61 0 3.09-.59 4.23-1.57l.27.28v.79l5 4.99L20.49 19l-4.99-5zm-6 0C7.01 14 5 11.99 5 9.5S7.01 5 9.5 5 14 7.01 14 9.5 11.99 14 9.5 14z"/>
                  </svg>
                </div>
                <h3 className="text-lg font-bold text-white">Strengthen <span className="text-blue-300">Surveillance</span></h3>
              </div>
            </div>
          </div>

          <Card className="border-0 shadow-xl bg-white/50 dark:bg-zinc-900/50 backdrop-blur-sm">
            <CardHeader>
              <CardTitle className="text-2xl font-bold text-slate-800 dark:text-slate-100">
                Our Commitment to Global Initiatives
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-6">
              <p className="text-slate-600 dark:text-slate-300 leading-relaxed">
                The UN SPECS framework represents a comprehensive approach to addressing visual impairment challenges globally. Each component plays a vital role in creating a more inclusive world. Through innovative technology and accessible design, iAssist contributes to these goals by providing a solution that helps individuals with visual impairments navigate their daily lives with greater independence and confidence.
              </p>
              <div className="bg-gradient-to-r from-blue-500/10 via-indigo-500/10 to-purple-500/10 dark:from-blue-500/20 dark:via-indigo-500/20 dark:to-purple-500/20 rounded-lg p-6">
                <p className="text-slate-700 dark:text-slate-200 font-medium italic">
                  "Our mission aligns with the UN's vision of a world where visual impairments no longer limit an individual's ability to live independently and participate fully in society." - the iAssist Team
                </p>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
}