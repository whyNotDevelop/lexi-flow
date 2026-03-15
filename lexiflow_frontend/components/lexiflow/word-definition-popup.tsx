"use client"

import { X, Bookmark, Volume2, BookOpen } from "lucide-react"
import { Button } from "@/components/ui/button"

interface Definition {
  meaning: string
  example: string
}

interface WordDefinitionPopupProps {
  word: string
  definitions: Definition[]
  isSaved: boolean
  onClose: () => void
  onSave: () => void
}

export function WordDefinitionPopup({ word, definitions, isSaved, onClose, onSave }: WordDefinitionPopupProps) {
  return (
    <>
      {/* Backdrop */}
      <div 
        className="absolute inset-0 bg-foreground/20 z-40"
        onClick={onClose}
      />
      
      {/* Popup */}
      <div className="absolute bottom-0 left-0 right-0 bg-card rounded-t-3xl shadow-2xl z-50 animate-in slide-in-from-bottom duration-300">
        {/* Handle */}
        <div className="flex justify-center pt-3">
          <div className="w-10 h-1 bg-border rounded-full" />
        </div>

        <div className="p-5">
          {/* Header */}
          <div className="flex items-start justify-between mb-4">
            <div>
              <h3 className="text-xl font-semibold text-foreground capitalize">{word}</h3>
              <p className="text-xs text-muted-foreground mt-0.5">/ {word.toLowerCase()} /</p>
            </div>
            <div className="flex items-center gap-2">
              <Button variant="ghost" size="icon" className="h-8 w-8 text-muted-foreground hover:text-primary">
                <Volume2 className="h-4 w-4" />
              </Button>
              <Button 
                variant="ghost" 
                size="icon" 
                className={`h-8 w-8 ${isSaved ? "text-primary" : "text-muted-foreground hover:text-primary"}`}
                onClick={onSave}
              >
                <Bookmark className={`h-4 w-4 ${isSaved ? "fill-current" : ""}`} />
              </Button>
              <Button variant="ghost" size="icon" className="h-8 w-8 text-muted-foreground" onClick={onClose}>
                <X className="h-4 w-4" />
              </Button>
            </div>
          </div>

          {/* Definitions */}
          <div className="space-y-4">
            {definitions.map((def, index) => (
              <div key={index} className="space-y-2">
                <div className="flex items-start gap-2">
                  <span className="flex items-center justify-center w-5 h-5 rounded-full bg-primary/10 text-primary text-xs font-medium shrink-0 mt-0.5">
                    {index + 1}
                  </span>
                  <p className="text-sm text-foreground leading-relaxed">{def.meaning}</p>
                </div>
                <div className="ml-7 flex items-start gap-2 text-muted-foreground">
                  <BookOpen className="h-3.5 w-3.5 mt-0.5 shrink-0" />
                  <p className="text-xs italic leading-relaxed">{`"${def.example}"`}</p>
                </div>
              </div>
            ))}
          </div>

          {/* Synonyms */}
          <div className="mt-5 pt-4 border-t border-border">
            <p className="text-xs font-medium text-muted-foreground mb-2">Synonyms</p>
            <div className="flex flex-wrap gap-2">
              {["Similar", "Related", "Akin"].map((syn, index) => (
                <span 
                  key={index}
                  className="px-2.5 py-1 bg-secondary text-secondary-foreground text-xs rounded-full"
                >
                  {syn}
                </span>
              ))}
            </div>
          </div>

          {/* Save button */}
          <Button 
            className="w-full mt-5"
            onClick={onSave}
            disabled={isSaved}
          >
            <Bookmark className="h-4 w-4 mr-2" />
            {isSaved ? "Saved to Vocabulary" : "Save to Vocabulary"}
          </Button>
        </div>
      </div>
    </>
  )
}
