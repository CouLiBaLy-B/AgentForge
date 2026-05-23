import React, { useState, useEffect } from 'react';
import { Plus, Play, GitPullRequest, CheckCircle, Loader2, Terminal, X } from 'lucide-react';

const COLUMNS = [
  { id: 'backlog', label: 'BACKLOG', color: 'text-slate-400' },
  { id: 'todo', label: 'TODO', color: 'text-yellow-400' },
  { id: 'in_progress', label: 'IN PROGRESS', color: 'text-blue-400' },
  { id: 'review', label: 'REVIEW', color: 'text-purple-400' },
  { id: 'done', label: 'DONE', color: 'text-green-400' },
  { id: 'failed', label: 'FAILED', color: 'text-red-400' }
];

export default function App() {
  const [tasks, setTasks] = useState([]);
  const [selectedTaskId, setSelectedTaskId] = useState(null);
  const [logs, setLogs] = useState([]);

  useEffect(() => {
    const socket = new WebSocket('ws://localhost:3000/ws/board');
    socket.onmessage = (event) => {
      const data = JSON.parse(event.data);
      if (data.type === 'task_created' || data.type === 'task_updated') {
        setTasks(prev => {
          const index = prev.findIndex(t => t.id === data.task.id);
          if (index > -1) {
            const newTasks = [...prev];
            newTasks[index] = data.task;
            return newTasks;
          }
          return [...prev, data.task];
        });
      }
    };
    return () => socket.close();
  }, []);

  // Poll for logs if a task is selected
  useEffect(() => {
    let interval;
    if (selectedTaskId) {
      const fetchLogs = async () => {
        try {
          const res = await fetch(`http://localhost:3000/api/tasks/${selectedTaskId}/logs`);
          const data = await res.json();
          setLogs(data.logs || []);
        } catch (e) { console.error(e); }
      };
      fetchLogs();
      interval = setInterval(fetchLogs, 3000);
    }
    return () => clearInterval(interval);
  }, [selectedTaskId]);

  const createTask = async () => {
    const title = prompt("Task title:");
    const repo = prompt("Repo (org/repo):", "CouLiBaLy-B/groupe-projets");
    if (title && repo) {
      await fetch(`http://localhost:3000/api/tasks?title=${encodeURIComponent(title)}&repo=${encodeURIComponent(repo)}`, { method: 'POST' });
    }
  };

  const startAgent = async (taskId) => {
    await fetch(`http://localhost:3000/api/tasks/${taskId}/start`, { method: 'POST' });
    setSelectedTaskId(taskId);
  };

  return (
    <div className="flex h-screen bg-[#0f172a] text-slate-200 overflow-hidden">
      {/* Main Board */}
      <div className={`flex-1 p-8 transition-all ${selectedTaskId ? 'mr-96' : ''}`}>
        <header className="flex justify-between items-center mb-10">
          <div>
            <h1 className="text-3xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-blue-400 to-emerald-400">
              AgentForge Board
            </h1>
          </div>
          <button onClick={createTask} className="flex items-center gap-2 bg-blue-600 hover:bg-blue-500 px-4 py-2 rounded-lg font-medium">
            <Plus size={20} /> New Task
          </button>
        </header>

        <div className="grid grid-cols-6 gap-4 overflow-x-auto pb-4">
          {COLUMNS.map(col => (
            <div key={col.id} className="min-w-[200px] bg-[#1e293b] rounded-xl p-4 min-h-[70vh]">
              <h2 className={`font-bold text-xs mb-4 flex justify-between items-center ${col.color}`}>
                {col.label}
                <span className="bg-slate-700 px-2 py-0.5 rounded text-slate-400">{tasks.filter(t => t.status === col.id).length}</span>
              </h2>
              <div className="space-y-3">
                {tasks.filter(t => t.status === col.id).map(task => (
                  <div 
                    key={task.id} 
                    onClick={() => setSelectedTaskId(task.id)}
                    className={`p-4 rounded-lg border cursor-pointer transition-all ${selectedTaskId === task.id ? 'bg-slate-700 border-blue-500' : 'bg-[#334155] border-slate-600 hover:border-slate-500'}`}
                  >
                    <div className="flex justify-between mb-2">
                      <span className="text-[10px] font-mono text-slate-500">#{task.id}</span>
                      {task.status === 'in_progress' && <Loader2 size={12} className="animate-spin text-blue-400" />}
                    </div>
                    <h3 className="text-sm font-medium leading-tight mb-2">{task.title}</h3>
                    <p className="text-[10px] text-slate-400">{task.repo}</p>
                    {task.status === 'backlog' && (
                      <button onClick={(e) => { e.stopPropagation(); startAgent(task.id); }} className="mt-3 w-full py-1 bg-slate-600 rounded text-[10px] flex items-center justify-center gap-1">
                        <Play size={10} /> Start Agent
                      </button>
                    )}
                  </div>
                ))}
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Side Log Panel */}
      {selectedTaskId && (
        <div className="fixed right-0 top-0 h-full w-96 bg-[#0b1120] border-l border-slate-800 flex flex-col shadow-2xl">
          <div className="p-4 border-b border-slate-800 flex justify-between items-center">
            <h2 className="flex items-center gap-2 font-bold text-sm">
              <Terminal size={16} className="text-emerald-400" /> Agent Activity
            </h2>
            <button onClick={() => setSelectedTaskId(null)} className="text-slate-500 hover:text-white">
              <X size={18} />
            </button>
          </div>
          <div className="flex-1 overflow-y-auto p-4 font-mono text-[11px] space-y-3">
            {logs.length === 0 && <p className="text-slate-600 italic">Waiting for logs...</p>}
            {logs.map((log, i) => (
              <div key={i} className="border-l-2 border-slate-700 pl-3 py-1">
                <div className="flex justify-between text-[9px] text-slate-500 mb-1">
                  <span>{log.agent.toUpperCase()}</span>
                  <span>{new Date(log.timestamp).toLocaleTimeString()}</span>
                </div>
                <div className="text-emerald-400 font-bold mb-0.5">{log.event}</div>
                <div className="text-slate-400 leading-relaxed">{log.details}</div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
