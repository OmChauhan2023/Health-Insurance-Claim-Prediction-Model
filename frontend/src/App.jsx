import { useState } from 'react'
import { Sun, Moon, Database } from 'lucide-react'
import Dashboard from './components/Dashboard'
import ChatPanel from './components/ChatPanel'

function App() {
  const [darkMode, setDarkMode] = useState(false)
  const [chatOpen, setChatOpen] = useState(false)

  const toggleDarkMode = () => {
    setDarkMode(!darkMode)
    if (!darkMode) {
      document.documentElement.classList.add('dark')
    } else {
      document.documentElement.classList.remove('dark')
    }
  }

  return (
    <div className="min-h-screen bg-zinc-50 dark:bg-[#09090b] text-zinc-950 dark:text-zinc-50 transition-colors duration-300 flex flex-col">
      {/* Header */}
      <header className="border-b border-zinc-200 dark:border-zinc-800 bg-white dark:bg-[#0c0c0f] sticky top-0 z-50">
        <div className="max-w-[1600px] mx-auto p-4 px-6 flex justify-between items-center">
          <div className="flex items-center gap-3">
            <div className="bg-blue-500 text-white p-2 rounded-lg">
              <Database size={24} />
            </div>
            <h1 className="text-xl font-bold tracking-tight">Health Insurance Claims Predictor</h1>
          </div>
          
          <div className="flex items-center gap-4">
            <button 
              onClick={() => setChatOpen(!chatOpen)}
              className="px-4 py-2 text-sm font-medium bg-blue-50 text-blue-600 hover:bg-blue-100 dark:bg-blue-900/30 dark:text-blue-400 dark:hover:bg-blue-900/50 rounded-lg transition-colors flex items-center gap-2"
            >
              Ask AI Data Analyst
            </button>
            <button 
              onClick={toggleDarkMode}
              className="p-2 text-zinc-500 hover:text-zinc-950 dark:text-zinc-400 dark:hover:text-zinc-50 transition-colors rounded-full hover:bg-zinc-100 dark:hover:bg-zinc-800"
            >
              {darkMode ? <Sun size={20} /> : <Moon size={20} />}
            </button>
          </div>
        </div>
      </header>

      {/* Main Content Area */}
      <div className="flex-1 max-w-[1600px] w-full mx-auto p-6 flex gap-6 relative">
        <div className={`transition-all duration-300 ease-in-out ${chatOpen ? 'w-2/3' : 'w-full'}`}>
          <Dashboard />
        </div>
        
        {/* Chat Panel Overlay / Side panel */}
        {chatOpen && (
          <div className="w-1/3 bg-white dark:bg-[#0c0c0f] rounded-xl border border-zinc-200 dark:border-zinc-800 shadow-xl overflow-hidden flex flex-col h-[calc(100vh-120px)] sticky top-[90px]">
             <ChatPanel onClose={() => setChatOpen(false)} />
          </div>
        )}
      </div>
    </div>
  )
}

export default App
