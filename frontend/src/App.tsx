import React, { useState, useEffect } from "react";
import { 
  Activity, 
  MapPin, 
  ShieldCheck, 
  Bell, 
  Settings, 
  History, 
  LayoutDashboard, 
  Search, 
  RefreshCw, 
  ExternalLink,
  ChevronRight,
  User,
  Zap,
  Globe,
  LogOut,
  Plus,
  PlusCircle,
  X
} from "lucide-react";
import { 
  XAxis, 
  YAxis, 
  CartesianGrid, 
  Tooltip, 
  ResponsiveContainer, 
  AreaChart, 
  Area 
} from 'recharts';
import axios from "axios";

const MOCK_CHART_DATA = [
  { time: '10:00', checks: 45, slots: 0 },
  { time: '11:00', checks: 52, slots: 1 },
  { time: '12:00', checks: 55, slots: 2 },
  { time: '12:30', checks: 67, slots: 0 },
  { time: '13:00', checks: 59, slots: 0 },
];

const API_BASE_URL = "/_/backend/api/v1";

export default function App() {
  const [activeTab, setActiveTab] = useState("dashboard");
  const [stats, setStats] = useState({ total_checks: 0, slots_found: 0, active_targets: 0, avg_latency: 0 });
  const [targets, setTargets] = useState<any[]>([]);
  const [logs, setLogs] = useState<any[]>([]);
  const [chartData, setChartData] = useState<any[]>(MOCK_CHART_DATA);

  const handleAddTarget = async () => {
    const country = prompt("Enter Country (e.g., France, Germany):");
    if (!country) return;
    const visaType = prompt("Enter Visa Type (e.g., Visa Appointment):") || "Visa Appointment";
    
    try {
      await axios.post(`${API_BASE_URL}/monitoring/targets`, {
        country,
        visa_type: visaType,
        status: "ACTIVE",
        config_json: { center: "Mumbai", portal_url: "https://www.vfsglobal.com/" }
      });
      // Refresh targets
      const targetsRes = await axios.get(`${API_BASE_URL}/monitoring/targets`);
      setTargets(targetsRes.data);
    } catch (e) {
      alert("Failed to add target.");
    }
  };

  useEffect(() => {
    const fetchData = async () => {
      try {
        const statsRes = await axios.get(`${API_BASE_URL}/monitoring/stats`);
        setStats(statsRes.data);

        const targetsRes = await axios.get(`${API_BASE_URL}/monitoring/targets`);
        setTargets(targetsRes.data);

        const logsRes = await axios.get(`${API_BASE_URL}/monitoring/logs`);
        setLogs(logsRes.data);

        const chartRes = await axios.get(`${API_BASE_URL}/monitoring/chart-data`);
        setChartData(chartRes.data);
      } catch (error) {

        console.error("Failed to fetch data from API", error);
      }
    };

    fetchData();
    const interval = setInterval(fetchData, 10000); 
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="flex h-screen bg-[#0d1117] text-white font-sans selection:bg-blue-500/30 overflow-hidden">
      {/* Sidebar - Hidden on tiny screens, flex-col on others */}
      <aside className="w-64 border-r border-white/5 bg-[#0d1117] hidden md:flex flex-col p-6 shrink-0">
        <div className="flex items-center gap-3 mb-10 px-2">
          <div className="w-10 h-10 bg-blue-600 rounded-xl flex items-center justify-center shadow-lg shadow-blue-600/20">
            <Zap size={22} className="text-white animate-pulse" />
          </div>
          <h1 className="text-xl font-black tracking-tighter">VFS<span className="text-blue-500">MAX</span></h1>
        </div>
        
        <nav className="flex-1 space-y-1">
          <NavItem icon={<LayoutDashboard size={18} />} label="Dashboard" active={activeTab === "dashboard"} onClick={() => setActiveTab("dashboard")} />
          <NavItem icon={<LogOut size={18} />} label="Logout" active={false} onClick={() => {}} />
        </nav>
        
        <div className="mt-auto pt-4 border-t border-white/5 px-2">
          <div className="flex items-center gap-3 py-2 bg-white/5 rounded-xl px-3 group hover:bg-white/10 clickable transition-all">
            <div className="w-8 h-8 bg-blue-500/20 rounded-full flex items-center justify-center">
              <User size={16} className="text-blue-400" />
            </div>
            <div className="flex-1 overflow-hidden">
              <p className="text-sm font-bold truncate tracking-tight">Mohammed Jarir Khan</p>
              <p className="text-[10px] text-blue-400 font-bold uppercase tracking-widest opacity-80">VFS Station Admin</p>
            </div>
          </div>
        </div>
      </aside>

      {/* Main Content */}
      <div className="flex-1 flex flex-col overflow-hidden">
        {/* Header */}
        <header className="h-16 border-b border-white/5 bg-[#0d1117]/50 backdrop-blur-sm flex items-center justify-between px-8">
          <div className="flex items-center gap-4">
            <h1 className="text-lg font-semibold tracking-tight capitalize">{activeTab}</h1>
            <div className="flex items-center gap-1.5 px-2 py-1 bg-green-500/10 rounded-full border border-green-500/20 glow-pulse-green">
              <div className="w-1.5 h-1.5 bg-green-500 rounded-full" />
              <p className="text-[8px] font-bold text-blue-400 uppercase tracking-tighter">Visa</p>
              <span className="text-[10px] font-bold text-green-400 uppercase tracking-widest">SYSTEM ONLINE</span>
            </div>
          </div>
          
          <div className="flex items-center gap-4">
             <button 
               onClick={async () => {
                 try {
                   await axios.post(`${API_BASE_URL}/monitoring/trigger-all`);
                   alert("Bot check iteration triggered!");
                 } catch (e) {
                   console.error(e);
                   alert("Failed to manual trigger.");
                 }
               }}
               className="flex items-center gap-2 px-4 py-2 bg-indigo-600/10 text-indigo-400 text-[10px] font-bold rounded-full border border-indigo-600/20 hover:bg-indigo-600 hover:text-white transition-all shadow-lg shadow-indigo-500/10 mr-2"
             >
               <Zap size={12} /> RUN BOT ITERATION
             </button>
             <div className="relative group">
                <Search size={18} className="absolute left-3 top-1/2 -translate-y-1/2 text-muted-foreground group-focus-within:text-blue-400 transition-colors" />
                <input 
                  type="text" 
                  placeholder="Search targets..." 
                  className="bg-white/5 border border-white/10 rounded-full py-1.5 pl-10 pr-4 text-sm w-64 focus:outline-none focus:ring-2 focus:ring-blue-500/40 transition-all font-light"
                />
             </div>
             <button className="p-2 hover:bg-white/5 rounded-full relative transition-colors">
               <Bell size={18} className="text-muted-foreground" />
               <div className="absolute top-2 right-2 w-2 h-2 bg-blue-500 rounded-full border-2 border-[#0d1117]" />
             </button>
          </div>
        </header>

          {/* Dashboard Content */}
        <main className="flex-1 overflow-y-auto p-4 md:p-8 space-y-6 scrollbar-thin scrollbar-thumb-white/10 scrollbar-track-transparent">
          
          {/* Stats Overview */}
          <div className="grid grid-cols-2 md:grid-cols-4 gap-3 md:gap-6">
            <StatCard icon={<Search size={20}/>} label="Checks Today" value={stats.total_checks.toString()} delta="+12%" color="blue" />
            <StatCard icon={<MapPin size={20}/>} label="Active Targets" value={stats.active_targets.toString()} subValue="Monitoring real-time" color="indigo" />
            <StatCard icon={<ShieldCheck size={20}/>} label="Slots Found" value={stats.slots_found.toString()} delta="+1" color="green" />
            <StatCard icon={<RefreshCw size={20}/>} label="Latency" value={`${stats.avg_latency}s`} color="amber" />
          </div>

          <div className="flex flex-col lg:grid lg:grid-cols-3 gap-6">
            <div className="lg:col-span-2 space-y-6">
              <section>
                <div className="flex items-center justify-between mb-4 px-1">
                  <h2 className="text-sm font-semibold text-muted-foreground uppercase tracking-widest">ACTIVE MONITORING TARGETS</h2>
                  <button 
                    onClick={handleAddTarget}
                    className="flex items-center gap-1.5 px-3 py-1 bg-blue-600 text-white text-[10px] font-bold rounded-full hover:bg-blue-500 transition-all shadow-lg shadow-blue-500/20"
                  >
                    <Plus size={12} /> ADD NEW TARGET
                  </button>
                </div>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  {targets.length > 0 ? targets.map(t => (
                        <TargetCard 
                            key={t.id}
                            id={t.id}
                            country={t.country} 
                            type={t.visa_type} 
                            location={t.config_json?.center || "Mumbai"} 
                            status={t.status} 
                            lastCheck="Active Now" 
                            health={95}
                            portalUrl={t.config_json?.portal_url}
                        />
                  )) : (
                    <div className="col-span-2 text-center py-12 glass-card border-dashed">
                        <Activity className="mx-auto text-muted-foreground/30 mb-2" size={32} />
                        <p className="text-sm text-muted-foreground">No active targets found. Add one to start monitoring.</p>
                    </div>
                  )}
                </div>
              </section>

              <section className="glass-card p-6">
                <div className="flex items-center justify-between mb-6">
                  <div>
                    <h3 className="text-lg font-semibold tracking-tight">System Performance</h3>
                    <p className="text-sm text-muted-foreground font-light">Global check frequency and slot detection rate (last 24h)</p>
                  </div>
                  <div className="flex gap-2">
                    <button className="px-3 py-1 text-xs bg-blue-600 rounded-lg font-medium hover:bg-blue-500 transition-colors shadow-lg shadow-blue-500/20">Realtime</button>
                    <button className="px-3 py-1 text-xs bg-white/5 rounded-lg font-medium hover:bg-white/10 transition-all">7 Days</button>
                  </div>
                </div>
                <div className="h-64 w-full">
                  <ResponsiveContainer width="100%" height="100%">
                    <AreaChart data={chartData}>
                      <defs>
                        <linearGradient id="colorChecks" x1="0" y1="0" x2="0" y2="1">
                          <stop offset="5%" stopColor="#3b82f6" stopOpacity={0.3}/>
                          <stop offset="95%" stopColor="#3b82f6" stopOpacity={0}/>
                        </linearGradient>
                      </defs>
                      <CartesianGrid strokeDasharray="3 3" stroke="#2a2e37" vertical={false} />
                      <XAxis dataKey="time" stroke="#60677a" fontSize={11} tickLine={false} axisLine={false} />
                      <YAxis stroke="#60677a" fontSize={11} tickLine={false} axisLine={false} />
                      <Tooltip 
                        contentStyle={{ backgroundColor: '#161b22', borderColor: '#30363d', borderRadius: '12px', fontSize: '12px' }}
                        itemStyle={{ color: '#3b82f6' }}
                      />
                      <Area type="monotone" dataKey="checks" stroke="#3b82f6" fillOpacity={1} fill="url(#colorChecks)" strokeWidth={2} />
                    </AreaChart>
                  </ResponsiveContainer>
                </div>
              </section>
            </div>

            <section className="flex flex-col">
              <div className="flex items-center justify-between mb-4 px-1">
                <h2 className="text-sm font-semibold text-muted-foreground uppercase tracking-widest">LIVE EVENT STREAM</h2>
                <div className="w-2 h-2 rounded-full bg-red-500 animate-ping" />
              </div>
              <div className="glass-card flex-1 p-4 overflow-hidden flex flex-col">
                <div className="space-y-4 flex-1 overflow-y-auto pr-2 scrollbar-thin">
                  {logs.length > 0 ? logs.map(l => (
                    <LogEntry 
                        key={l.id} 
                        time={new Date(l.timestamp).toLocaleTimeString()} 
                        status={l.status === 'SUCCESS' ? 'SUCCESS' : l.status === 'ERROR' ? 'ERROR' : 'INFO'} 
                        msg={l.message || 'Check completed'} 
                        target={l.target_id.toString()} 
                    />
                  )) : (
                    <div className="text-center py-20 opacity-20 italic text-xs">Awaiting first system event...</div>
                  )}
                </div>

                <div className="mt-4 pt-4 border-t border-white/5">
                   <button className="w-full py-2 bg-blue-600/10 text-blue-400 text-xs font-bold rounded-lg hover:bg-blue-600/20 transition-all tracking-widest">CLEAR STREAM</button>
                </div>
              </div>
            </section>
          </div>
        </main>
      </div>
    </div>
  );
}

interface NavItemProps {
  icon: React.ReactNode;
  label: string;
  active?: boolean;
  onClick: () => void;
}

function NavItem({ icon, label, active = false, onClick }: NavItemProps) {
  return (
    <button 
      onClick={onClick}
      className={`w-full flex items-center gap-3 px-4 py-2.5 rounded-xl transition-all duration-300 group
        ${active ? 'bg-blue-600 text-white shadow-xl shadow-blue-600/20' : 'text-muted-foreground hover:bg-white/5 hover:text-white'}`}
    >
      <span className={`${active ? 'text-white' : 'group-hover:text-blue-400'}`}>{icon}</span>
      <span className="text-sm font-medium tracking-tight">{label}</span>
      {active && <ChevronRight size={14} className="ml-auto opacity-60" />}
    </button>
  );
}

interface StatCardProps {
  icon: React.ReactNode;
  label: string;
  value: string;
  delta?: string;
  subValue?: string;
  color: 'blue' | 'indigo' | 'green' | 'amber';
}

function StatCard({ icon, label, value, delta, subValue, color }: StatCardProps) {
  const colorMap: Record<string, string> = {
    blue: 'bg-blue-500/10 text-blue-400 border-blue-500/20',
    indigo: 'bg-indigo-500/10 text-indigo-400 border-indigo-500/20',
    green: 'bg-emerald-500/10 text-emerald-400 border-emerald-500/20',
    amber: 'bg-amber-500/10 text-amber-400 border-amber-500/20',
  };
  
  return (
    <div className="glass-card hover:translate-y-[-4px] transition-all duration-300 group p-5 flex flex-col justify-between h-32 relative overflow-hidden">
      <div className={`absolute -right-8 -top-8 w-24 h-24 blur-[60px] opacity-20 pointer-events-none rounded-full ${color === 'blue' ? 'bg-blue-500' : color === 'green' ? 'bg-emerald-500' : 'bg-indigo-500'}`} />
      
      <div className="flex justify-between items-start">
        <div className={`p-2 rounded-xl border ${colorMap[color]}`}>
          {icon}
        </div>
        {delta && <span className="text-[10px] font-bold text-emerald-400 bg-emerald-400/10 px-2 py-0.5 rounded-full border border-emerald-400/20">{delta}</span>}
      </div>
      <div>
        <p className="text-xs text-muted-foreground font-light mb-0.5">{label}</p>
        <div className="flex items-baseline gap-2">
          <p className="text-2xl font-bold tracking-tight">{value}</p>
          {subValue && <span className="text-[10px] text-muted-foreground/60">{subValue}</span>}
        </div>
      </div>
    </div>
  );
}

interface TargetCardProps {
  id: number;
  country: string;
  type: string;
  location: string;
  status: string;
  lastCheck: string;
  health: number;
  portalUrl?: string;
}

function TargetCard({ id, country, type, location, status, lastCheck, health, portalUrl }: TargetCardProps) {
  const triggerCheck = async () => {
    try {
      await axios.post(`${API_BASE_URL}/monitoring/targets/${id}/check`);
      alert(`Manual check triggered for ${country}`);
    } catch (e) {
      console.error(e);
      alert("Failed to trigger check. Ensure backend is running.");
    }
  };

  return (
    <div className="glass-card p-5 group hover:border-blue-500/30 transition-all duration-300 relative">
      <div className="flex justify-between mb-4">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 bg-white/5 rounded-xl border border-white/5 flex items-center justify-center p-2">
             <Globe size={24} className="text-blue-400" />
          </div>
          <div>
            <h4 className="font-semibold text-sm tracking-tight">{country} - {location}</h4>
            <p className="text-xs text-muted-foreground">{type}</p>
          </div>
        </div>
        <div className="flex flex-col items-end">
           <span className="text-[10px] font-bold text-green-400 flex items-center gap-1">
             <div className="w-1.5 h-1.5 bg-green-400 rounded-full glow-pulse-green" />
             {status}
           </span>
           <span className="text-[10px] text-muted-foreground mt-0.5 font-light">{lastCheck}</span>
        </div>
      </div>
      
      <div className="space-y-3">
        <div className="flex justify-between text-[11px] font-medium text-muted-foreground">
          <span>Target Status</span>
          <span className="text-blue-400 capitalize">{status.toLowerCase()}</span>
        </div>
        <div className="h-1.5 w-full bg-white/5 rounded-full overflow-hidden">
          <div className="h-full bg-green-500 rounded-full shadow-[0_0_8px_rgba(34,197,94,0.5)] w-full" />
        </div>
      </div>

      <div className="mt-5 grid grid-cols-2 gap-3 opacity-0 group-hover:opacity-100 translate-y-2 group-hover:translate-y-0 transition-all duration-300">
         <button 
           onClick={triggerCheck}
           className="flex items-center justify-center gap-2 py-1.5 bg-blue-600/10 text-blue-400 text-xs font-bold rounded-lg border border-blue-600/20 hover:bg-blue-600 hover:text-white transition-all"
         >
           <RefreshCw size={14} /> CHECK NOW
         </button>
         <button 
           onClick={() => portalUrl && window.open(portalUrl, '_blank')}
           className="flex items-center justify-center gap-2 py-1.5 bg-white/5 text-white text-xs font-bold rounded-lg border border-white/5 hover:bg-white/10 transition-all"
         >
           <ExternalLink size={14} /> PORTAL
         </button>
      </div>
    </div>
  );
}

interface LogEntryProps {
  time: string;
  status: 'INFO' | 'SUCCESS' | 'ERROR' | 'WARN';
  msg: string;
  target?: string;
}

function LogEntry({ time, status, msg, target }: LogEntryProps) {
  const statusColors: Record<string, string> = {
    INFO: 'text-blue-400',
    SUCCESS: 'text-emerald-400',
    ERROR: 'text-rose-400',
    WARN: 'text-amber-400'
  };

  return (
    <div className="text-[11px] font-mono leading-relaxed group py-1 border-b border-white/[0.02] last:border-0">
      <span className="text-muted-foreground/40">{time}</span>
      <span className={`mx-2 font-bold ${statusColors[status] || 'text-white/50'}`}>[{status}]</span>
      <span className="text-white/80">{msg}</span>
      {target && <span className="opacity-0 group-hover:opacity-100 text-[10px] bg-blue-500/10 text-blue-400 px-1.5 py-0.5 rounded ml-2 transition-opacity">{target}</span>}
    </div>
  );
}
