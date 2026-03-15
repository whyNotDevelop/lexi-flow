"use client"

import { Book, Bookmark, Settings, ChevronRight, User, Bell, Moon, Globe, Shield, HelpCircle, LogOut } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Switch } from "@/components/ui/switch"

interface SettingsScreenProps {
  onNavigate: (screen: string) => void
  isDarkMode: boolean
  onToggleDarkMode: () => void
}

const settingsGroups = [
  {
    title: "Account",
    items: [
      { icon: User, label: "Profile", hasArrow: true },
      { icon: Bell, label: "Notifications", hasArrow: true },
    ]
  },
  {
    title: "Preferences",
    items: [
      { icon: Moon, label: "Dark Mode", hasSwitch: true },
      { icon: Globe, label: "Language", value: "English", hasArrow: true },
    ]
  },
  {
    title: "About",
    items: [
      { icon: Shield, label: "Privacy Policy", hasArrow: true },
      { icon: HelpCircle, label: "Help & Support", hasArrow: true },
    ]
  }
]

export function SettingsScreen({ onNavigate, isDarkMode, onToggleDarkMode }: SettingsScreenProps) {
  return (
    <div className="h-full flex flex-col bg-background">
      {/* Header */}
      <div className="px-5 pt-3 pb-4">
        <h1 className="text-xl font-semibold text-foreground">Settings</h1>
      </div>

      {/* Profile card */}
      <div className="px-5 mb-4">
        <div className="flex items-center gap-3 p-4 bg-card rounded-xl border border-border">
          <div className="w-12 h-12 rounded-full bg-primary/10 flex items-center justify-center">
            <span className="text-lg font-semibold text-primary">JD</span>
          </div>
          <div className="flex-1">
            <h3 className="font-medium text-foreground">John Doe</h3>
            <p className="text-xs text-muted-foreground">john@example.com</p>
          </div>
          <ChevronRight className="h-5 w-5 text-muted-foreground" />
        </div>
      </div>

      {/* Settings list */}
      <div className="flex-1 overflow-y-auto px-5">
        <div className="space-y-5">
          {settingsGroups.map((group, groupIndex) => (
            <div key={groupIndex}>
              <p className="text-xs font-medium text-muted-foreground mb-2 px-1">{group.title}</p>
              <div className="bg-card rounded-xl border border-border overflow-hidden">
                {group.items.map((item, itemIndex) => (
                  <div 
                    key={itemIndex}
                    className={`flex items-center justify-between p-3 ${itemIndex !== group.items.length - 1 ? "border-b border-border" : ""}`}
                  >
                    <div className="flex items-center gap-3">
                      <div className="w-8 h-8 rounded-lg bg-secondary flex items-center justify-center">
                        <item.icon className="h-4 w-4 text-foreground" />
                      </div>
                      <span className="text-sm text-foreground">{item.label}</span>
                    </div>
                    {item.hasSwitch ? (
                      <Switch 
                        checked={item.label === "Dark Mode" ? isDarkMode : false}
                        onCheckedChange={item.label === "Dark Mode" ? onToggleDarkMode : undefined}
                      />
                    ) : item.hasArrow ? (
                      <div className="flex items-center gap-2">
                        {item.value && (
                          <span className="text-xs text-muted-foreground">{item.value}</span>
                        )}
                        <ChevronRight className="h-4 w-4 text-muted-foreground" />
                      </div>
                    ) : null}
                  </div>
                ))}
              </div>
            </div>
          ))}

          {/* Logout */}
          <Button variant="ghost" className="w-full justify-start text-destructive hover:text-destructive hover:bg-destructive/10">
            <LogOut className="h-4 w-4 mr-2" />
            Log Out
          </Button>
        </div>

        <p className="text-center text-xs text-muted-foreground mt-6 mb-4">
          LexiFlow v1.0.0
        </p>
      </div>

      {/* Bottom navigation */}
      <div className="flex items-center justify-around py-3 border-t border-border bg-card">
        <Button 
          variant="ghost" 
          size="sm" 
          className="flex flex-col items-center gap-1 h-auto py-2"
          onClick={() => onNavigate("reading")}
        >
          <Book className="h-5 w-5 text-muted-foreground" />
          <span className="text-xs text-muted-foreground">Reading</span>
        </Button>
        <Button 
          variant="ghost" 
          size="sm" 
          className="flex flex-col items-center gap-1 h-auto py-2"
          onClick={() => onNavigate("vocabulary")}
        >
          <Bookmark className="h-5 w-5 text-muted-foreground" />
          <span className="text-xs text-muted-foreground">Vocabulary</span>
        </Button>
        <Button 
          variant="ghost" 
          size="sm" 
          className="flex flex-col items-center gap-1 h-auto py-2"
          onClick={() => onNavigate("history")}
        >
          <svg className="h-5 w-5 text-muted-foreground" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
          <span className="text-xs text-muted-foreground">History</span>
        </Button>
        <Button variant="ghost" size="sm" className="flex flex-col items-center gap-1 h-auto py-2">
          <Settings className="h-5 w-5 text-primary" />
          <span className="text-xs text-primary font-medium">Settings</span>
        </Button>
      </div>
    </div>
  )
}
