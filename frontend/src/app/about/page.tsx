"use client";
import { FaGithub, FaLinkedin } from "react-icons/fa";
import Link from "next/link";
import Image from "next/image";
import {BackgroundGradient} from "@/components/ui/background-gradient";
import {AnimatedText} from "@/components/ui/animated-underline-text-one";

export default function AboutPage() {
  return (
    <div className="max-w-5xl mx-auto py-12 px-4">
      <section className="mb-20">
        <div className="text-center mb-12">
          <AnimatedText 
            text="About iAssist"
            textClassName="text-5xl font-extrabold bg-gradient-to-r from-blue-500 via-blue-600 to-indigo-600 bg-clip-text text-transparent"
            underlineClassName="text-blue-500 dark:text-blue-400"
          />
        </div>
        
        <div className="grid md:grid-cols-2 gap-12 items-center">
          <div className="relative rounded-xl overflow-hidden shadow-2xl">
            <div className="aspect-[16/9] bg-gradient-to-r from-blue-500 via-indigo-500 to-indigo-600 flex items-center justify-center p-8">
            </div>
          </div>

          <div>
            <h2 className="text-2xl font-bold mb-4 text-slate-800 dark:text-slate-100">Our Mission</h2>
            <p className="text-slate-700 dark:text-slate-200 leading-relaxed">
              Using advanced AI technology, we provide real-time audio descriptions of surroundings, 
              obstacles, and potential hazards. Our goal is to empower users with technology that 
              enhances their daily independence and safety.
            </p>
          </div>
        </div>
      </section>
      <section>
        <h2 className="text-3xl font-bold text-center mb-12 text-slate-800 dark:text-slate-100">Meet Our Team</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
          {/* Shium */}
          <div className="relative isolate">
            <BackgroundGradient className="rounded-[22px] bg-white dark:bg-zinc-900">
              <div className="p-6 flex flex-col items-center justify-center">
                <Image
                  src="/team/shium.png"
                  alt="Shium Mashud"
                  width={128}
                  height={128}
                  className="w-32 h-32 rounded-full overflow-hidden bg-slate-200 dark:bg-slate-700"
                />
                <h3 className="text-xl font-semibold mt-4 text-slate-800 dark:text-slate-100">Shium Mashud</h3>
                <p className="text-blue-600 dark:text-blue-400 font-medium mb-2">Backend/AI Modeling</p>
                <div className="flex justify-center gap-4 mb-4">
                  <Link href="https://linkedin.com/in/shium" target="_blank" rel="noopener noreferrer" className="text-2xl hover:text-blue-600 transition-colors">
                    <FaLinkedin />
                  </Link>
                  <Link href="https://github.com/shiumash" target="_blank" rel="noopener noreferrer" className="text-2xl hover:text-gray-600 transition-colors">
                    <FaGithub />
                  </Link>
                </div>
                <p className="text-sm text-slate-600 dark:text-slate-300 text-center leading-relaxed">
                  CS + Engineering at University of Connecticut, interested in software design, and large-scale Big Data infrastructure
                </p>
              </div>
            </BackgroundGradient>
          </div>

          {/* Soonwho */}
          <div className="relative isolate">
            <BackgroundGradient className="rounded-[22px] bg-white dark:bg-zinc-900">
              <div className="p-6 flex flex-col items-center justify-center">
                <Image
                  src="/team/Soonwoo.png"
                  alt="Soonwoo Kwon"
                  width={128}
                  height={128}
                  className="w-32 h-32 rounded-full overflow-hidden bg-slate-200 dark:bg-slate-700"
                />
                <h3 className="text-xl font-semibold mt-4 text-slate-800 dark:text-slate-100">Soonwoo Kwon</h3>
                <p className="text-blue-600 dark:text-blue-400 font-medium mb-2">Backend/AI Modeling</p>
                <div className="flex justify-center gap-4 mb-4">
                  <Link href="https://www.linkedin.com/in/soonwook/" target="_blank" rel="noopener noreferrer" className="text-2xl hover:text-blue-600 transition-colors">
                    <FaLinkedin />
                  </Link>
                  <Link href="https://github.com/swoonyk" target="_blank" rel="noopener noreferrer" className="text-2xl hover:text-gray-600 transition-colors">
                    <FaGithub />
                  </Link>
                </div>
                <p className="text-sm text-slate-600 dark:text-slate-300 text-center leading-relaxed">
                  CS at University of Connecticut, interested in full-stack development, as well as Bayesian methodologies
                </p>
              </div>
            </BackgroundGradient>
          </div>

          {/* Richard */}
          <div className="relative isolate">
            <BackgroundGradient className="rounded-[22px] bg-white dark:bg-zinc-900">
              <div className="p-6 flex flex-col items-center justify-center">
                <Image
                  src="/team/Richard.png"
                  alt="Richard Li"
                  width={128}
                  height={128}
                  className="w-32 h-32 rounded-full overflow-hidden bg-slate-200 dark:bg-slate-700"
                />
                <h3 className="text-xl font-semibold mt-4 text-slate-800 dark:text-slate-100">Richard Li</h3>
                <p className="text-blue-600 dark:text-blue-400 font-medium mb-2">Frontend</p>
                <div className="flex justify-center gap-4 mb-4">
                  <Link href="https://www.linkedin.com/in/richardli14/" target="_blank" rel="noopener noreferrer" className="text-2xl hover:text-blue-600 transition-colors">
                    <FaLinkedin />
                  </Link>
                  <Link href="https://github.com/dkyxhjj" target="_blank" rel="noopener noreferrer" className="text-2xl hover:text-gray-600 transition-colors">
                    <FaGithub />
                  </Link>
                </div>
                <p className="text-sm text-slate-600 dark:text-slate-300 text-center leading-relaxed">
                  Data Science + Statistics at UCLA, interested in machine learning, graphic designing, sports analytics and fullstack development
                </p>
              </div>
            </BackgroundGradient>
          </div>

          {/* Annie */}
          <div className="relative isolate">
            <BackgroundGradient className="rounded-[22px] bg-white dark:bg-zinc-900">
              <div className="p-6 flex flex-col items-center justify-center">
                <Image
                  src="/team/Annie.png"
                  alt="Annie Dong"
                  width={128}
                  height={128}
                  className="w-32 h-32 rounded-full overflow-hidden bg-slate-200 dark:bg-slate-700"
                />
                <h3 className="text-xl font-semibold mt-4 text-slate-800 dark:text-slate-100">Annie Dong</h3>
                <p className="text-blue-600 dark:text-blue-400 font-medium mb-2">Backend</p>
                <div className="flex justify-center gap-4 mb-4">
                  <Link href="https://www.linkedin.com/in/annieydong/" target="_blank" rel="noopener noreferrer" className="text-2xl hover:text-blue-600 transition-colors">
                    <FaLinkedin />
                  </Link>
                  <Link href="https://github.com/annniedong" target="_blank" rel="noopener noreferrer" className="text-2xl hover:text-gray-600 transition-colors">
                    <FaGithub />
                  </Link>
                </div>
                <p className="text-sm text-slate-600 dark:text-slate-300 text-center leading-relaxed">
                  CS at Barnard University, interested in computer science, artificial intelligence, and interdisciplinary research
                </p>
              </div>
            </BackgroundGradient>
          </div>
        </div>
      </section>
    </div>
  );
}