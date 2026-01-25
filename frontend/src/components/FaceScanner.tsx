'use client'

import { useState, useRef, useEffect } from 'react'
import { Camera, Upload, ArrowRight, X } from 'lucide-react'

interface FaceScannerProps {
  onEmotionDetected: (emotions: { [key: string]: number }, moodScore: number) => void
  onClose: () => void
}

export default function FaceScanner({ onEmotionDetected, onClose }: FaceScannerProps) {
  const videoRef = useRef<HTMLVideoElement>(null)
  const canvasRef = useRef<HTMLCanvasElement>(null)
  const [isLoading, setIsLoading] = useState(true)
  const [isScanning, setIsScanning] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [detectedEmotions, setDetectedEmotions] = useState<{ [key: string]: number } | null>(null)
  const [modelsLoaded, setModelsLoaded] = useState(false)
  const [faceapi, setFaceapi] = useState<any>(null)
  const [imageMode, setImageMode] = useState(false)
  const [uploadedImage, setUploadedImage] = useState<string | null>(null)
  const imageRef = useRef<HTMLImageElement>(null)
  const intervalRef = useRef<NodeJS.Timeout | null>(null)

  // Dynamically load face-api.js (client-side only)
  useEffect(() => {
    const loadFaceApi = async () => {
      try {
        const faceApiModule = await import('face-api.js')
        setFaceapi(faceApiModule)
      } catch (err) {
        console.error('Error loading face-api.js:', err)
        setError('Face detection library could not be loaded.')
        setIsLoading(false)
      }
    }
    loadFaceApi()
  }, [])

  // Load face-api.js models from CDN
  useEffect(() => {
    if (!faceapi) return

    const loadModels = async () => {
      try {
        // Use CDN for models (jsdelivr CDN)
        const MODEL_URL = 'https://cdn.jsdelivr.net/npm/@vladmandic/face-api/model'
        await Promise.all([
          faceapi.nets.tinyFaceDetector.loadFromUri(MODEL_URL),
          faceapi.nets.faceLandmark68Net.loadFromUri(MODEL_URL),
          faceapi.nets.faceRecognitionNet.loadFromUri(MODEL_URL),
          faceapi.nets.faceExpressionNet.loadFromUri(MODEL_URL),
        ])
        setModelsLoaded(true)
        setIsLoading(false)
      } catch (err) {
        console.error('Error loading models:', err)
        // Try alternative CDN
        try {
          const ALT_MODEL_URL = 'https://raw.githubusercontent.com/justadudewhohacks/face-api.js/master/weights'
          await Promise.all([
            faceapi.nets.tinyFaceDetector.loadFromUri(ALT_MODEL_URL),
            faceapi.nets.faceLandmark68Net.loadFromUri(ALT_MODEL_URL),
            faceapi.nets.faceRecognitionNet.loadFromUri(ALT_MODEL_URL),
            faceapi.nets.faceExpressionNet.loadFromUri(ALT_MODEL_URL),
          ])
          setModelsLoaded(true)
          setIsLoading(false)
        } catch (err2) {
          console.error('Error loading from alternative CDN:', err2)
          setError('Face detection models could not be loaded. Please check your internet connection.')
          setIsLoading(false)
        }
      }
    }
    loadModels()
  }, [faceapi])

  // Start camera
  useEffect(() => {
    if (!modelsLoaded) return

    const startCamera = async () => {
      try {
        const stream = await navigator.mediaDevices.getUserMedia({
          video: { width: 640, height: 480, facingMode: 'user' }
        })
        if (videoRef.current) {
          videoRef.current.srcObject = stream
        }
      } catch (err) {
        console.error('Error accessing camera:', err)
        setError('Could not access camera. Please check permissions.')
        setIsLoading(false)
      }
    }

    startCamera()

    return () => {
      if (videoRef.current?.srcObject) {
        const stream = videoRef.current.srcObject as MediaStream
        stream.getTracks().forEach(track => track.stop())
      }
      if (intervalRef.current) {
        clearInterval(intervalRef.current)
      }
    }
  }, [modelsLoaded])

  // Detect emotions from video
  const detectEmotions = async () => {
    if (!videoRef.current || !canvasRef.current || !modelsLoaded || !faceapi) return

    const video = videoRef.current
    const canvas = canvasRef.current
    
    // Wait for video to have valid dimensions
    if (video.videoWidth === 0 || video.videoHeight === 0) {
      return null
    }

    const displaySize = { width: video.videoWidth, height: video.videoHeight }

    // Set canvas dimensions to match video
    canvas.width = video.videoWidth
    canvas.height = video.videoHeight

    faceapi.matchDimensions(canvas, displaySize)

    const detections = await faceapi
      .detectAllFaces(video, new faceapi.TinyFaceDetectorOptions())
      .withFaceLandmarks()
      .withFaceExpressions()

    const resizedDetections = faceapi.resizeResults(detections, displaySize)
    
    // Clear canvas
    const ctx = canvas.getContext('2d')
    if (ctx) {
      ctx.clearRect(0, 0, canvas.width, canvas.height)
    }

    // Draw detections
    faceapi.draw.drawDetections(canvas, resizedDetections)
    faceapi.draw.drawFaceLandmarks(canvas, resizedDetections)
    faceapi.draw.drawFaceExpressions(canvas, resizedDetections)

    if (detections.length > 0) {
      const expressions = detections[0].expressions
      setDetectedEmotions(expressions)
      
      // Calculate mood score from emotions
      const moodScore = calculateMoodScore(expressions)
      
      return { expressions, moodScore }
    }

    return null
  }

  const calculateMoodScore = (expressions: { [key: string]: number }): number => {
    // Map emotions to mood score (0-10)
    const positiveEmotions = ['happy', 'surprised']
    const negativeEmotions = ['sad', 'angry', 'fearful', 'disgusted']
    
    let score = 5.0 // Neutral
    
    for (const [emotion, value] of Object.entries(expressions)) {
      if (positiveEmotions.includes(emotion)) {
        score += value * 3
      } else if (negativeEmotions.includes(emotion)) {
        score -= value * 3
      }
    }
    
    return Math.max(0, Math.min(10, score))
  }

  // Detect emotions from uploaded image
  const detectEmotionsFromImage = async () => {
    if (!imageRef.current || !canvasRef.current || !modelsLoaded || !faceapi) return

    const image = imageRef.current
    const canvas = canvasRef.current
    
    // Wait for image to load
    if (image.naturalWidth === 0 || image.naturalHeight === 0) {
      return null
    }

    const displaySize = { width: image.naturalWidth, height: image.naturalHeight }

    // Set canvas dimensions to match image
    canvas.width = image.naturalWidth
    canvas.height = image.naturalHeight

    faceapi.matchDimensions(canvas, displaySize)

    const detections = await faceapi
      .detectAllFaces(image, new faceapi.TinyFaceDetectorOptions())
      .withFaceLandmarks()
      .withFaceExpressions()

    const resizedDetections = faceapi.resizeResults(detections, displaySize)
    
    // Clear canvas
    const ctx = canvas.getContext('2d')
    if (ctx) {
      ctx.clearRect(0, 0, canvas.width, canvas.height)
      // Draw the image first
      ctx.drawImage(image, 0, 0, canvas.width, canvas.height)
    }

    // Draw detections
    faceapi.draw.drawDetections(canvas, resizedDetections)
    faceapi.draw.drawFaceLandmarks(canvas, resizedDetections)
    faceapi.draw.drawFaceExpressions(canvas, resizedDetections)

    if (detections.length > 0) {
      const expressions = detections[0].expressions
      setDetectedEmotions(expressions)
      
      // Calculate mood score from emotions
      const moodScore = calculateMoodScore(expressions)
      
      return { expressions, moodScore }
    }

    return null
  }

  const handleImageUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0]
    if (!file) return

    // Validate file type
    if (!file.type.startsWith('image/')) {
      setError('Please upload an image file (jpg, png, etc.)')
      return
    }

    // Validate file size (max 10MB)
    if (file.size > 10 * 1024 * 1024) {
      setError('Image file is too large. Please use an image under 10MB.')
      return
    }

    const reader = new FileReader()
    reader.onload = (event) => {
      const imageUrl = event.target?.result as string
      setUploadedImage(imageUrl)
      setImageMode(true)
      setError(null)
      
      // Wait for image to load, then detect
      setTimeout(() => {
        detectEmotionsFromImage()
      }, 100)
    }
    reader.onerror = () => {
      setError('Failed to read image file.')
    }
    reader.readAsDataURL(file)
  }

  const startScanning = () => {
    setIsScanning(true)
    setDetectedEmotions(null)
    
    // Scan every 500ms
    intervalRef.current = setInterval(async () => {
      await detectEmotions()
    }, 500)
  }

  const stopScanning = () => {
    setIsScanning(false)
    if (intervalRef.current) {
      clearInterval(intervalRef.current)
      intervalRef.current = null
    }
  }

  const captureEmotion = async () => {
    stopScanning()
    const result = imageMode 
      ? await detectEmotionsFromImage()
      : await detectEmotions()
    
    if (result) {
      onEmotionDetected(result.expressions, result.moodScore)
      onClose()
    } else {
      setError(imageMode 
        ? 'No face detected in the image. Please try a different image.'
        : 'No face detected. Please position your face in front of the camera.')
    }
  }

  const resetToCamera = () => {
    setImageMode(false)
    setUploadedImage(null)
    setDetectedEmotions(null)
    setError(null)
    // Restart camera
    if (videoRef.current && modelsLoaded) {
      navigator.mediaDevices.getUserMedia({
        video: { width: 640, height: 480, facingMode: 'user' }
      }).then(stream => {
        if (videoRef.current) {
          videoRef.current.srcObject = stream
        }
      })
    }
  }

  if (isLoading) {
    return (
      <div className="fixed inset-0 bg-black/50 backdrop-blur-sm z-50 flex items-center justify-center">
        <div className="bg-white/10 backdrop-blur-md rounded-2xl p-8 border border-white/20 shadow-lg">
          <div className="flex flex-col items-center gap-4">
            <svg className="animate-spin h-8 w-8 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
              <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
              <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
            <p className="text-white font-medium">Loading face detection models...</p>
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="fixed inset-0 bg-black/50 backdrop-blur-sm z-50 flex items-center justify-center p-4 overflow-y-auto">
      <div className="bg-white/10 backdrop-blur-md rounded-2xl p-6 border border-white/20 shadow-lg max-w-4xl w-full my-8">
        <div className="flex justify-between items-center mb-4">
          <h3 className="text-2xl font-bold text-white drop-shadow-sm">Face Mood Scanner</h3>
          <button
            onClick={onClose}
            className="text-white/80 hover:text-white text-2xl font-bold"
          >
            <X className="w-6 h-6" />
          </button>
        </div>

        {error && (
          <div className="mb-4 p-4 bg-red-500/20 border border-red-400/50 rounded-lg text-white backdrop-blur-sm">
            {error}
          </div>
        )}

        {/* Mode Toggle */}
        <div className="flex gap-2 mb-4">
          <button
            onClick={() => {
              if (imageMode) resetToCamera()
            }}
            className={`flex-1 py-2 px-4 rounded-xl font-medium transition-all duration-200 ${
              !imageMode
                ? 'bg-white text-green-800'
                : 'bg-white/10 text-white hover:bg-white/20 border border-white/20'
            }`}
          >
            <Camera className="w-4 h-4" /> Camera
          </button>
          <button
            onClick={() => setImageMode(true)}
            className={`flex-1 py-2 px-4 rounded-xl font-medium transition-all duration-200 ${
              imageMode
                ? 'bg-white text-green-800'
                : 'bg-white/10 text-white hover:bg-white/20 border border-white/20'
            }`}
          >
            <Upload className="w-4 h-4" /> Upload Image
          </button>
        </div>

        {/* Image Upload Input */}
        {imageMode && !uploadedImage && (
          <div className="mb-4">
            <label className="block w-full">
              <div className="border-2 border-dashed border-white/30 rounded-xl p-8 text-center cursor-pointer hover:border-white/50 transition-all">
                <p className="text-white font-medium mb-2">Click to upload an image</p>
                <p className="text-green-50/80 text-sm">JPG, PNG up to 10MB</p>
                <input
                  type="file"
                  accept="image/*"
                  onChange={handleImageUpload}
                  className="hidden"
                />
              </div>
            </label>
          </div>
        )}

        {/* Video/Image Display */}
        <div className="relative mb-4 rounded-xl overflow-hidden bg-black flex items-center justify-center" style={{ maxHeight: '75vh', minHeight: '300px' }}>
          {imageMode && uploadedImage ? (
            <>
              <img
                ref={imageRef}
                src={uploadedImage}
                alt="Uploaded"
                className="object-contain"
                style={{ 
                  maxWidth: '100%', 
                  maxHeight: '75vh',
                  width: 'auto', 
                  height: 'auto',
                  display: 'block'
                }}
                onLoad={() => {
                  // Detect emotions when image loads
                  if (modelsLoaded && faceapi) {
                    setTimeout(() => detectEmotionsFromImage(), 100)
                  }
                }}
              />
              <canvas
                ref={canvasRef}
                className="absolute top-0 left-0 w-full h-full pointer-events-none"
              />
            </>
          ) : (
            <>
              <video
                ref={videoRef}
                autoPlay
                muted
                playsInline
                className="w-full h-auto max-h-[70vh] object-contain"
                style={{ transform: 'scaleX(-1)' }}
                onLoadedMetadata={(e) => {
                  // Ensure canvas is sized when video loads
                  if (canvasRef.current && videoRef.current) {
                    canvasRef.current.width = videoRef.current.videoWidth
                    canvasRef.current.height = videoRef.current.videoHeight
                  }
                }}
              />
              <canvas
                ref={canvasRef}
                className="absolute top-0 left-0 w-full h-full pointer-events-none"
                style={{ transform: 'scaleX(-1)' }}
              />
            </>
          )}
        </div>

        {detectedEmotions && (
          <div className="mb-4 p-4 bg-white/5 rounded-xl border border-white/20">
            <p className="text-green-50 font-medium mb-2">Detected Emotions:</p>
            <div className="flex flex-wrap gap-2">
              {Object.entries(detectedEmotions)
                .filter(([_, value]) => value > 0.1)
                .sort(([_, a], [__, b]) => b - a)
                .map(([emotion, value]) => (
                  <span
                    key={emotion}
                    className="px-3 py-1 bg-white/10 rounded-full text-white text-sm font-medium border border-white/20"
                  >
                    {emotion}: {(value * 100).toFixed(0)}%
                  </span>
                ))}
            </div>
          </div>
        )}

        <div className="flex gap-3">
          {imageMode ? (
            <>
              <button
                onClick={resetToCamera}
                className="flex-1 bg-white/20 text-white py-3 px-6 rounded-xl font-medium hover:bg-white/30 transition-all duration-300 border border-white/30"
              >
                Use Camera
              </button>
              <button
                onClick={captureEmotion}
                className="flex-1 bg-white text-green-800 py-3 px-6 rounded-xl font-bold hover:bg-green-50 hover:shadow-[0_0_20px_rgba(255,255,255,0.4)] transition-all duration-300"
              >
                Analyze Mood
              </button>
            </>
          ) : (
            <>
              {!isScanning ? (
                <button
                  onClick={startScanning}
                  className="flex-1 bg-white text-green-800 py-3 px-6 rounded-xl font-bold hover:bg-green-50 hover:shadow-[0_0_20px_rgba(255,255,255,0.4)] transition-all duration-300"
                >
                  Start Scanning
                </button>
              ) : (
                <>
                  <button
                    onClick={stopScanning}
                    className="flex-1 bg-white/20 text-white py-3 px-6 rounded-xl font-medium hover:bg-white/30 transition-all duration-300 border border-white/30"
                  >
                    Stop
                  </button>
                  <button
                    onClick={captureEmotion}
                    className="flex-1 bg-white text-green-800 py-3 px-6 rounded-xl font-bold hover:bg-green-50 hover:shadow-[0_0_20px_rgba(255,255,255,0.4)] transition-all duration-300"
                  >
                    Capture Mood
                  </button>
                </>
              )}
            </>
          )}
        </div>

        <p className="text-green-50/80 text-sm mt-4 text-center">
          {imageMode 
            ? 'Upload an image with a face to analyze mood'
            : 'Position your face in front of the camera and click "Start Scanning"'}
        </p>
      </div>
    </div>
  )
}

