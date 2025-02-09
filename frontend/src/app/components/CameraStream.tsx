'use client'

import { useState, useEffect } from 'react'
import { io } from 'socket.io-client'

export function CameraStream() {
  const [status, setStatus] = useState<string>('Connecting...')
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const socket = io('http://localhost:5003')

    socket.on('connect', () => {
      setStatus('Connected')
      setError(null)
    })

    socket.on('camera_error', (data: any) => {
      setError(data.message)
    })

    socket.on('status', (data: any) => {
      setStatus(data.message)
    })

    return () => {
      socket.disconnect()
    }
  }, [])


  return (
    <div className="relative w-full aspect-video">
      {error ? (
        <p className="text-red-500">{error}</p>
      ) : (
        <>
          <img
            src="http://localhost:5003/video_feed"
            alt="Camera feed"
            className="w-full h-full object-contain"
          />
          <p className="absolute top-2 right-2 bg-black/50 text-white px-2 py-1 rounded">
            {status}
          </p>
        </>
      )}
    </div>
  )
}