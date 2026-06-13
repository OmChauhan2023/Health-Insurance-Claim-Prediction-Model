import { useState, useCallback } from 'react'
import { Sun, Moon, ShieldCheck, BrainCircuit, BarChart3, Search, MessageSquare, X } from 'lucide-react'
import Dashboard from './components/Dashboard'
import ModelDev from './components/ModelDev'
import Analytics from './components/Analytics'
import PlotsGallery from './components/PlotsGallery'
import ChatPanel from './components/ChatPanel'

const TABS = [
  { id: 'home',      label: 'Home',              Icon: ShieldCheck },
  { id: 'model',     label: 'Model Development', Icon: BrainCircuit },
  { id: 'analytics', label: 'Analytics & Results', Icon: BarChart3 },
  { id: 'plots',     label: 'Feature Intelligence', Icon: Search },
]

function App() {
  const [darkMode, setDarkMode] = useState(false)
  const [activeTab, setActiveTab] = useState('home')
  const [chatOpen, setChatOpen] = useState(false)

  const toggleDarkMode = useCallback(() => {
    setDarkMode(prev => {
      const next = !prev
      if (next) {
        document.documentElement.classList.add('dark')
      } else {
        document.documentElement.classList.remove('dark')
      }
      return next
    })
  }, [])

  return (
    <div className="min-h-screen bg-zinc-50 dark:bg-[#09090b] text-zinc-950 dark:text-zinc-50 transition-colors duration-300">

      {/* ── Top Navigation Bar ── */}
      <header className="border-b border-zinc-200 dark:border-zinc-800 bg-white dark:bg-[#0c0c0f] sticky top-0 z-50">
        <div className="max-w-[1600px] mx-auto px-6 h-14 flex items-center justify-between gap-6">

          {/* Brand */}
          <div className="flex items-center gap-2.5 shrink-0">
            <div className="bg-gradient-to-br from-blue-500 to-indigo-600 text-white p-1.5 rounded-lg">
              <ShieldCheck size={20} />
            </div>
            <span className="font-bold text-base tracking-tight whitespace-nowrap">ZebraInsure<span className="text-blue-500">AI</span></span>
          </div>

          {/* Tab Nav */}
          <nav className="flex items-center gap-1 overflow-x-auto">
            {TABS.map(({ id, label, Icon }) => (
              <button
                key={id}
                onClick={() => setActiveTab(id)}
                className={`flex items-center gap-1.5 px-3.5 py-1.5 rounded-lg text-sm font-medium whitespace-nowrap transition-all duration-150 ${
                  activeTab === id
                    ? 'bg-blue-50 text-blue-600 dark:bg-blue-900/30 dark:text-blue-400'
                    : 'text-zinc-500 hover:text-zinc-800 dark:hover:text-zinc-200 hover:bg-zinc-100 dark:hover:bg-zinc-800'
                }`}
              >
                <Icon size={15} />
                {label}
              </button>
            ))}
          </nav>

          {/* Right controls */}
          <div className="flex items-center gap-2 shrink-0">
            <button
              onClick={() => setChatOpen(o => !o)}
              className={`flex items-center gap-2 px-3 py-1.5 rounded-lg text-sm font-medium transition-all ${
                chatOpen
                  ? 'bg-blue-600 text-white shadow-lg shadow-blue-500/30'
                  : 'bg-blue-50 text-blue-600 hover:bg-blue-100 dark:bg-blue-900/30 dark:text-blue-400 dark:hover:bg-blue-900/50'
              }`}
            >
              <MessageSquare size={15} />
              AI Analyst
            </button>
            <button
              onClick={toggleDarkMode}
              className="p-2 rounded-lg text-zinc-500 hover:text-zinc-900 dark:text-zinc-400 dark:hover:text-zinc-50 hover:bg-zinc-100 dark:hover:bg-zinc-800 transition-colors"
            >
              {darkMode ? <Sun size={18} /> : <Moon size={18} />}
            </button>
          </div>
        </div>
      </header>

      {/* ── Body: tab content + chat panel side-by-side ── */}
      <div className="max-w-[1600px] mx-auto px-6 py-6 flex gap-6 items-start">

        {/* Main content */}
        <div className={`flex-1 min-w-0 transition-all duration-300 ${chatOpen ? 'max-w-[calc(100%-380px)]' : 'max-w-full'}`}>
          {activeTab === 'home'      && <Dashboard />}
          {activeTab === 'model'     && <ModelDev />}
          {activeTab === 'analytics' && <Analytics />}
          {activeTab === 'plots'     && <PlotsGallery />}
        </div>

        {/* Slide-in Chat Panel */}
        {chatOpen && (
          <div className="w-[360px] shrink-0 sticky top-[72px] h-[calc(100vh-96px)] bg-white dark:bg-[#0c0c0f] rounded-xl border border-zinc-200 dark:border-zinc-800 shadow-2xl shadow-zinc-200/60 dark:shadow-black/40 flex flex-col overflow-hidden">
            <ChatPanel onClose={() => setChatOpen(false)} />
          </div>
        )}
      </div>
    </div>
  )
}

export default App
