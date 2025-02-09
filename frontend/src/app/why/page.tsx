"use client";

import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import {
  Chart as ChartJS,
  ArcElement,
  Tooltip,
  Legend,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
} from 'chart.js';
import { Doughnut } from 'react-chartjs-2';
import type { ChartOptions } from 'chart.js';

ChartJS.register(
  ArcElement,
  Tooltip,
  Legend,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement
);

export default function WhyPage() {
  const chartData = {
    labels: ['Population affected by visual impairments (billions)', 'Population without visual impairments (billions)'],
    datasets: [
      {
        data: [2.2, 5.8],
        backgroundColor: [
          'rgb(79, 70, 229)',
          'rgb(229, 231, 235)',
        ],
        borderColor: [
          'rgb(79, 70, 229)',
          'rgb(229, 231, 235)',
        ],
        borderWidth: 1,
      },
    ],
  };

  const chartOptions: ChartOptions<'doughnut'> = {
    responsive: true,
    plugins: {
      legend: {
        onClick: (e: any) => e.stopPropagation(),
        position: 'bottom' as const,
        labels: {
          padding: 20,
          font: {
            size: 14
          }
        }
      },
      tooltip: {
        enabled: true,
        backgroundColor: 'rgba(0, 0, 0, 0.8)',
        titleFont: {
          size: 14
        },
        bodyFont: {
          size: 14
        },
        callbacks: {
          label: function(context: any) {
            return `${context.raw} billion people`;
          }
        }
      },
      title: {
        display: true,
        text: 'Global Impact of Visual Impairments',
        font: {
          size: 18,
          weight: 'bold'
        },
        padding: {
          top: 10,
          bottom: 20
        }
      }
    },
    animation: {
      duration: 0
    },
    interaction: {
      mode: 'nearest',
      intersect: true,
    },
    cutout: '60%',
    elements: {
      arc: {
        borderWidth: 1,
      }
    },
  };

  return (
    <div className="space-y-8 p-6 max-w-7xl mx-auto">

      {/* Statistics Section */}
      <div className="space-y-6">
        <h2 className="text-4xl font-semibold text-center mb-8">Why iAssist?</h2>
        <Card>
          <CardHeader>
            <CardTitle>Proportion of People with Visual Impairments</CardTitle>
            <CardDescription>Global distribution of visual impairment cases</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="w-full h-[400px] flex items-center justify-center">
              <div className="w-[400px] h-[400px]">
                <Doughnut 
                  data={chartData} 
                  options={chartOptions}
                />
              </div>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* SPECS Goals */}
      <div className="space-y-6">
        <h2 className="text-2xl font-semibold">UN SPECS Goals for Visual Accessibility</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-5 gap-4">
          {/* Services */}
          <div className="bg-indigo-900 text-white p-6 rounded-xl flex flex-col items-center text-center space-y-4">
            <div className="w-12 h-12 text-yellow-400">
              <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor">
                <path d="M12 3c-4.97 0-9 4.03-9 9s4.03 9 9 9 9-4.03 9-9-4.03-9-9-9zm0 16c-3.87 0-7-3.13-7-7s3.13-7 7-7 7 3.13 7 7-3.13 7-7 7zm-.5-4.5c-.83 0-1.5-.67-1.5-1.5s.67-1.5 1.5-1.5 1.5.67 1.5 1.5-.67 1.5-1.5 1.5z"/>
              </svg>
            </div>
            <h3 className="text-lg font-semibold">Improve access to refractive <span className="text-yellow-400">Services</span></h3>
          </div>

          {/* Personnel */}
          <div className="bg-indigo-900 text-white p-6 rounded-xl flex flex-col items-center text-center space-y-4">
            <div className="w-12 h-12 text-yellow-400">
              <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor">
                <path d="M16 11c1.66 0 2.99-1.34 2.99-3S17.66 5 16 5s-3 1.34-3 3 1.34 3 3 3zm-8 0c1.66 0 2.99-1.34 2.99-3S9.66 5 8 5 5 6.34 5 8s1.34 3 3 3zm0 2c-2.33 0-7 1.17-7 3.5V19h14v-2.5c0-2.33-4.67-3.5-7-3.5zm8 0c-.29 0-.62.02-.97.05 1.16.84 1.97 1.97 1.97 3.45V19h6v-2.5c0-2.33-4.67-3.5-7-3.5z"/>
              </svg>
            </div>
            <h3 className="text-lg font-semibold">Build capacity of <span className="text-yellow-400">Personnel</span> to provide refractive services</h3>
          </div>

          {/* Education */}
          <div className="bg-indigo-900 text-white p-6 rounded-xl flex flex-col items-center text-center space-y-4">
            <div className="w-12 h-12 text-yellow-400">
              <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor">
                <path d="M21 17v-6.9L12 15 1 9l11-6 11 6v8h-2zm-9 4l-7-3.8v-8.37L12 13l7-3.8v8.37L12 21z"/>
              </svg>
            </div>
            <h3 className="text-lg font-semibold">Improve population <span className="text-yellow-400">Education</span></h3>
          </div>

          {/* Cost */}
          <div className="bg-indigo-900 text-white p-6 rounded-xl flex flex-col items-center text-center space-y-4">
            <div className="w-12 h-12 text-yellow-400">
              <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor">
                <path d="M11.8 10.9c-2.27-.59-3-1.2-3-2.15 0-1.09 1.01-1.85 2.7-1.85 1.78 0 2.44.85 2.5 2.1h2.21c-.07-1.72-1.12-3.3-3.21-3.81V3h-3v2.16c-1.94.42-3.5 1.68-3.5 3.61 0 2.31 1.91 3.46 4.7 4.13 2.5.6 3 1.48 3 2.41 0 .69-.49 1.79-2.7 1.79-2.06 0-2.87-.92-2.98-2.1h-2.2c.12 2.19 1.76 3.42 3.68 3.83V21h3v-2.15c1.95-.37 3.5-1.5 3.5-3.55 0-2.84-2.43-3.81-4.7-4.4z"/>
              </svg>
            </div>
            <h3 className="text-lg font-semibold">Reduce the <span className="text-yellow-400">Cost</span> of refractive services</h3>
          </div>

          {/* Surveillance */}
          <div className="bg-indigo-900 text-white p-6 rounded-xl flex flex-col items-center text-center space-y-4">
            <div className="w-12 h-12 text-yellow-400">
              <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor">
                <path d="M15.5 14h-.79l-.28-.27C15.41 12.59 16 11.11 16 9.5 16 5.91 13.09 3 9.5 3S3 5.91 3 9.5 5.91 16 9.5 16c1.61 0 3.09-.59 4.23-1.57l.27.28v.79l5 4.99L20.49 19l-4.99-5zm-6 0C7.01 14 5 11.99 5 9.5S7.01 5 9.5 5 14 7.01 14 9.5 11.99 14 9.5 14z"/>
              </svg>
            </div>
            <h3 className="text-lg font-semibold">Strengthen <span className="text-yellow-400">Surveillance</span> and research</h3>
          </div>
        </div>
      </div>
    </div>
  );
}