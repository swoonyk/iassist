"use client";
import { FaGithub, FaLinkedin } from "react-icons/fa";
import Link from "next/link";
import Image from "next/image";

export default function AboutPage() {
  return (
    <div className="max-w-5xl mx-auto py-12 px-4">
      <section className="text-center mb-16">
        <h1 className="text-5xl font-extrabold bg-gradient-to-r from-blue-600 to-indigo-600 bg-clip-text text-transparent mb-8">
          iAssist
        </h1>
        
        <div className="grid md:grid-cols-2 gap-8 items-center">
        <div className="relative rounded-xl overflow-hidden shadow-2xl">
            <div className="aspect-[16/9] bg-gradient-to-r from-blue-500 to-indigo-600 flex items-center justify-center p-8">
            </div>
          </div>

          <div className="text-left">
            <p className="text-xl text-muted-foreground mb-8">
              iAssist is an innovative computer vision application designed to help visually impaired individuals
              navigate their environment with greater confidence and independence. Using advanced AI technology,
              we provide real-time audio descriptions of surroundings, obstacles, and potential hazards.
            </p>
          </div>

        </div>
      </section>

      <section>
        <h2 className="text-3xl font-bold text-center mb-12">Meet Our Team</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
          {/* Shium */}
          <div className="text-center">
            <div className="w-32 h-32 mx-auto mb-4 rounded-full overflow-hidden bg-slate-200 dark:bg-slate-700 flex items-center justify-center">
            <Image
                src="/team/shium.png"
                alt="Shium Mashud"
                width={128}
                height={128}
                className="object-cover w-full h-full"
              />
            </div>
            <h3 className="text-xl font-semibold mb-2">Shium Mashud</h3>
            <p className="text-muted-foreground mb-2">Backend/AI Modeling</p>
            <div className="flex justify-center gap-4 mb-4">
              <Link href="https://linkedin.com/in/shium" target="_blank" rel="noopener noreferrer" className="text-2xl hover:text-blue-600 transition-colors">
                <FaLinkedin />
              </Link>
              <Link href="https://github.com/shiumash" target="_blank" rel="noopener noreferrer" className="text-2xl hover:text-gray-600 transition-colors">
                <FaGithub />
              </Link>
            </div>
            <p className="text-sm text-muted-foreground mb-4">
              CS + Engineering at University of Connecticut, interested in full-stack application development, software design, and large-scale Big Data infrastructure
            </p>
          </div>

          {/* Soonwho */}
          <div className="text-center">
            <div className="w-32 h-32 mx-auto mb-4 rounded-full overflow-hidden bg-slate-200 dark:bg-slate-700 flex items-center justify-center">
            <Image
                src="/team/Soonwoo.png"
                alt="Soonwoo Kwon"
                width={128}
                height={128}
                className="object-cover w-full h-full"
              />
            </div>
            <h3 className="text-xl font-semibold mb-2">Soonwoo Kwon</h3>
            <p className="text-muted-foreground mb-2">Backend/AI Modeling</p>
            <div className="flex justify-center gap-4 mb-4">
              <Link href="https://www.linkedin.com/in/soonwook/" target="_blank" rel="noopener noreferrer" className="text-2xl hover:text-blue-600 transition-colors">
                <FaLinkedin />
              </Link>
              <Link href="https://github.com/swoonyk" target="_blank" rel="noopener noreferrer" className="text-2xl hover:text-gray-600 transition-colors">
                <FaGithub />
              </Link>
            </div>
            <p className="text-sm text-muted-foreground mb-4">
              CS at University of Connecticut, interested in full-stack development, as well as Bayesian methodologies
            </p>
            
          </div>

          {/* Richard */}
          <div className="text-center">
            <div className="w-32 h-32 mx-auto mb-4 rounded-full overflow-hidden bg-slate-200 dark:bg-slate-700">
              <Image
                src="/team/Richard.png"
                alt="Richard Li"
                width={128}
                height={128}
                className="object-cover w-full h-full"
              />
            </div>
            <h3 className="text-xl font-semibold mb-2">Richard Li</h3>
            <p className="text-muted-foreground mb-2">Frontend</p>
            <div className="flex justify-center gap-4 mb-4">
              <Link href="https://www.linkedin.com/in/richardli14/" target="_blank" rel="noopener noreferrer" className="text-2xl hover:text-blue-600 transition-colors">
                <FaLinkedin />
              </Link>
              <Link href="https://github.com/dkyxhjj" target="_blank" rel="noopener noreferrer" className="text-2xl hover:text-gray-600 transition-colors">
                <FaGithub />
              </Link>
            </div>
            <p className="text-sm text-muted-foreground mb-4">
              Data Science + Statistics at UCLA, interested in machine learning, graphic designing, sports analytics and fullstack development
            </p>
          </div>

          {/* Annie */}
          <div className="text-center">
            <div className="w-32 h-32 mx-auto mb-4 rounded-full overflow-hidden bg-slate-200 dark:bg-slate-700 flex items-center justify-center">
            <Image
                src="/team/Annie.png"
                alt="Annie Dong"
                width={128}
                height={128}
                className="object-cover w-full h-full"
              />
            </div>
            <h3 className="text-xl font-semibold mb-2">Annie Dong</h3>
            <p className="text-muted-foreground mb-2">Backend</p>
            <div className="flex justify-center gap-4 mb-4">
              <Link href="https://www.linkedin.com/in/annieydong/" target="_blank" rel="noopener noreferrer" className="text-2xl hover:text-blue-600 transition-colors">
                <FaLinkedin />
              </Link>
              <Link href="https://github.com/annniedong" target="_blank" rel="noopener noreferrer" className="text-2xl hover:text-gray-600 transition-colors">
                <FaGithub />
              </Link>
            </div>
            <p className="text-sm text-muted-foreground">
              CS at Barnard University, interested in computer science, artificial intelligence, and interdisciplinary research
            </p>
            
          </div>
        </div>
      </section>
    </div>
  );
}