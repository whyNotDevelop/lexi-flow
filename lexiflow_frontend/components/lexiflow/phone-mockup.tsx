"use client"

import { ReactNode } from "react"

interface PhoneMockupProps {
  children: ReactNode
  className?: string
}

export function PhoneMockup({ children, className = "" }: PhoneMockupProps) {
  return (
    <div className={`relative mx-auto ${className}`}>
      {/* Phone frame */}
      <div className="relative w-[320px] h-[680px] bg-foreground rounded-[3rem] p-3 shadow-2xl">
        {/* Inner bezel */}
        <div className="relative w-full h-full bg-background rounded-[2.25rem] overflow-hidden">
          {/* Notch */}
          <div className="absolute top-0 left-1/2 -translate-x-1/2 w-32 h-7 bg-foreground rounded-b-2xl z-50" />
          
          {/* Status bar */}
          <div className="absolute top-0 left-0 right-0 h-12 flex items-center justify-between px-8 z-40">
            <span className="text-xs font-medium text-foreground">9:41</span>
            <div className="flex items-center gap-1">
              <svg className="w-4 h-4 text-foreground" fill="currentColor" viewBox="0 0 24 24">
                <path d="M12 3C7.46 3 3.34 4.78.29 7.67c-.18.18-.29.43-.29.71 0 .28.11.53.29.71l2.48 2.48c.18.18.43.29.71.29.27 0 .52-.11.7-.28.79-.74 1.69-1.36 2.66-1.85.33-.16.56-.5.56-.9v-3.1c1.45-.48 3-.73 4.6-.73s3.15.25 4.6.73v3.1c0 .4.23.74.56.9.98.49 1.87 1.12 2.67 1.85.18.18.43.28.7.28.28 0 .53-.11.71-.29l2.48-2.48c.18-.18.29-.43.29-.71 0-.28-.11-.53-.29-.71C20.66 4.78 16.54 3 12 3z"/>
              </svg>
              <svg className="w-4 h-4 text-foreground" fill="currentColor" viewBox="0 0 24 24">
                <path d="M15.67 4H14V2h-4v2H8.33C7.6 4 7 4.6 7 5.33v15.33C7 21.4 7.6 22 8.33 22h7.33c.74 0 1.34-.6 1.34-1.33V5.33C17 4.6 16.4 4 15.67 4z"/>
              </svg>
            </div>
          </div>

          {/* Screen content */}
          <div className="h-full pt-12 pb-2">
            {children}
          </div>

          {/* Home indicator */}
          <div className="absolute bottom-2 left-1/2 -translate-x-1/2 w-32 h-1 bg-foreground/30 rounded-full" />
        </div>
      </div>
    </div>
  )
}
