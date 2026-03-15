"use client"

import { useState, useEffect } from "react"
import { PhoneMockup } from "./phone-mockup"
import { LoginScreen } from "./login-screen"
import { ReadingScreen } from "./reading-screen"
import { VocabularyScreen } from "./vocabulary-screen"
import { HistoryScreen } from "./history-screen"
import { SettingsScreen } from "./settings-screen"

type Screen = "login" | "reading" | "vocabulary" | "history" | "settings"

export function LexiFlowApp() {
  const [currentScreen, setCurrentScreen] = useState<Screen>("login")
  const [isLoggedIn, setIsLoggedIn] = useState(false)
  const [isDarkMode, setIsDarkMode] = useState(false)

  useEffect(() => {
    if (isDarkMode) {
      document.documentElement.classList.add("dark")
    } else {
      document.documentElement.classList.remove("dark")
    }
  }, [isDarkMode])

  const handleLogin = () => {
    setIsLoggedIn(true)
    setCurrentScreen("reading")
  }

  const handleNavigate = (screen: string) => {
    setCurrentScreen(screen as Screen)
  }

  const toggleDarkMode = () => {
    setIsDarkMode(!isDarkMode)
  }

  const renderScreen = () => {
    if (!isLoggedIn) {
      return <LoginScreen onLogin={handleLogin} />
    }

    switch (currentScreen) {
      case "reading":
        return (
          <ReadingScreen 
            onNavigate={handleNavigate} 
            isDarkMode={isDarkMode}
            onToggleDarkMode={toggleDarkMode}
          />
        )
      case "vocabulary":
        return <VocabularyScreen onNavigate={handleNavigate} />
      case "history":
        return <HistoryScreen onNavigate={handleNavigate} />
      case "settings":
        return (
          <SettingsScreen 
            onNavigate={handleNavigate}
            isDarkMode={isDarkMode}
            onToggleDarkMode={toggleDarkMode}
          />
        )
      default:
        return (
          <ReadingScreen 
            onNavigate={handleNavigate}
            isDarkMode={isDarkMode}
            onToggleDarkMode={toggleDarkMode}
          />
        )
    }
  }

  return (
    <PhoneMockup>
      {renderScreen()}
    </PhoneMockup>
  )
}
