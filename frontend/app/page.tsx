'use client';

import { useEffect, useState } from 'react';
import {
  fetchProgramStats,
  fetchYearStats,
  fetchDivisionStats,
  fetchLifetimeStats,
  fetchYearlyBreakdown,
  fetchEnrollments,
  fetchPlayerEnrollmentStats,
} from '@/lib/api';
import {
  BarChart,
  Bar,
  LineChart,
  Line,
  PieChart,
  Pie,
  Cell,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from 'recharts';
import { Activity, Users, TrendingUp, Calendar } from 'lucide-react';

interface ProgramStats {
  ProgramName: string;
  ProgramYear: number;
  PlayerCount: number;
  FamilyCount: number;
}

interface YearStats {
  ProgramYear: number;
  UniquePlayerCount: number;
  UniqueFamilyCount: number;
}

interface DivisionStats {
  ProgramYear: number;
  ProgramName: string;
  DivisionName: string;
  Players: number;
}

interface LifetimeStats {
  PlayersLifetime: number;
  FamiliesLifetime: number;
}

interface YearlyBreakdown {
  [year: string]: {
    players: number;
    families: number;
  };
}

interface PlayerEnrollmentStats {
  PlayerId: number;
  PlayerFirstName: string;
  PlayerLastName: string;
  TotalEnrollments: number;
}

const COLORS = ['#0ea5e9', '#8b5cf6', '#ec4899', '#f59e0b', '#10b981', '#ef4444'];

export default function Home() {
  const [programStats, setProgramStats] = useState<ProgramStats[]>([]);
  const [yearStats, setYearStats] = useState<YearStats[]>([]);
  const [divisionStats, setDivisionStats] = useState<DivisionStats[]>([]);
  const [lifetimeStats, setLifetimeStats] = useState<LifetimeStats | null>(null);
  const [yearlyBreakdown, setYearlyBreakdown] = useState<YearlyBreakdown | null>(null);
  const [enrollments, setEnrollments] = useState<any[]>([]);
  const [playerEnrollmentStats, setPlayerEnrollmentStats] = useState<PlayerEnrollmentStats[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const loadData = async () => {
      try {
        setLoading(true);
        const [programs, years, divisions, lifetime, yearly, enrollData, playerEnrolls] = await Promise.all([
          fetchProgramStats(),
          fetchYearStats(),
          fetchDivisionStats(),
          fetchLifetimeStats(),
          fetchYearlyBreakdown(),
          fetchEnrollments({ limit: 50 }),
          fetchPlayerEnrollmentStats(50),
        ]);

        setProgramStats(programs);
        setYearStats(years);
        setDivisionStats(divisions);
        setLifetimeStats(lifetime);
        setYearlyBreakdown(yearly);
        setEnrollments(enrollData);
        setPlayerEnrollmentStats(playerEnrolls);
      } catch (err) {
        setError('Failed to load data. Please check if the backend is running.');
        console.error(err);
      } finally {
        setLoading(false);
      }
    };

    loadData();
  }, []);

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading dashboard...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <div className="text-center bg-red-50 p-8 rounded-lg border border-red-200">
          <p className="text-red-600 font-semibold">{error}</p>
          <p className="text-sm text-gray-600 mt-2">Make sure Docker containers are running.</p>
        </div>
      </div>
    );
  }

  const yearlyData = yearlyBreakdown
    ? Object.entries(yearlyBreakdown).map(([year, data]) => ({
        year,
        players: data.players,
        families: data.families,
      }))
    : [];

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 py-6 sm:px-6 lg:px-8">
          <h1 className="text-3xl font-bold text-gray-900">LPFC Athletic Programs Dashboard</h1>
          <p className="text-gray-600 mt-1">Enrollment and Program Statistics</p>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 py-8 sm:px-6 lg:px-8">
        {/* Stats Cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <div className="bg-white rounded-lg shadow p-6 border-l-4 border-primary-500">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600">Total Players</p>
                <p className="text-3xl font-bold text-gray-900 mt-2">
                  {lifetimeStats?.PlayersLifetime || 0}
                </p>
              </div>
              <div className="bg-primary-100 rounded-full p-3">
                <Users className="w-8 h-8 text-primary-600" />
              </div>
            </div>
          </div>

          <div className="bg-white rounded-lg shadow p-6 border-l-4 border-purple-500">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600">Total Families</p>
                <p className="text-3xl font-bold text-gray-900 mt-2">
                  {lifetimeStats?.FamiliesLifetime || 0}
                </p>
              </div>
              <div className="bg-purple-100 rounded-full p-3">
                <Activity className="w-8 h-8 text-purple-600" />
              </div>
            </div>
          </div>

          <div className="bg-white rounded-lg shadow p-6 border-l-4 border-pink-500">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600">Programs</p>
                <p className="text-3xl font-bold text-gray-900 mt-2">
                  {programStats.length}
                </p>
              </div>
              <div className="bg-pink-100 rounded-full p-3">
                <TrendingUp className="w-8 h-8 text-pink-600" />
              </div>
            </div>
          </div>

          <div className="bg-white rounded-lg shadow p-6 border-l-4 border-orange-500">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600">Active Years</p>
                <p className="text-3xl font-bold text-gray-900 mt-2">
                  {yearStats.length}
                </p>
              </div>
              <div className="bg-orange-100 rounded-full p-3">
                <Calendar className="w-8 h-8 text-orange-600" />
              </div>
            </div>
          </div>
        </div>

        {/* Charts Row 1 */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
          {/* Yearly Trends */}
          <div className="bg-white rounded-lg shadow p-6">
            <h2 className="text-xl font-bold text-gray-900 mb-4">Yearly Trends</h2>
            <ResponsiveContainer width="100%" height={300}>
              <LineChart data={yearlyData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="year" />
                <YAxis />
                <Tooltip />
                <Legend />
                <Line
                  type="monotone"
                  dataKey="players"
                  stroke="#0ea5e9"
                  strokeWidth={2}
                  name="Players"
                />
                <Line
                  type="monotone"
                  dataKey="families"
                  stroke="#8b5cf6"
                  strokeWidth={2}
                  name="Families"
                />
              </LineChart>
            </ResponsiveContainer>
          </div>

          {/* Year Statistics */}
          <div className="bg-white rounded-lg shadow p-6">
            <h2 className="text-xl font-bold text-gray-900 mb-4">Players by Year</h2>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={yearStats}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="ProgramYear" />
                <YAxis />
                <Tooltip />
                <Legend />
                <Bar dataKey="UniquePlayerCount" fill="#0ea5e9" name="Players" />
                <Bar dataKey="UniqueFamilyCount" fill="#8b5cf6" name="Families" />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Program Statistics Bar Chart */}
        <div className="bg-white rounded-lg shadow p-6 mb-8">
          <h2 className="text-xl font-bold text-gray-900 mb-4">Program Enrollment</h2>
          <ResponsiveContainer width="100%" height={Math.max(500, programStats.length * 45)}>
            <BarChart
              data={programStats.map((stat: ProgramStats) => ({
                ...stat,
                displayName: `${stat.ProgramYear} - ${stat.ProgramName}`
              }))}
              layout="vertical"
              margin={{ left: 30, right: 20 }}
            >
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis type="number" />
              <YAxis
                dataKey="displayName"
                type="category"
                width={350}
                tick={{ fontSize: 11 }}
                interval={0}
              />
              <Tooltip />
              <Legend />
              <Bar dataKey="PlayerCount" fill="#0ea5e9" name="Players" />
              <Bar dataKey="FamilyCount" fill="#8b5cf6" name="Families" />
            </BarChart>
          </ResponsiveContainer>
        </div>

        {/* Division Statistics Table */}
        <div className="bg-white rounded-lg shadow p-6 mb-8">
          <h2 className="text-xl font-bold text-gray-900 mb-4">Division Statistics</h2>
          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Year
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Program
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Division
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Gender
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Players
                  </th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {divisionStats.slice(0, 20).map((stat, index) => (
                  <tr key={index} className="hover:bg-gray-50">
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                      {stat.ProgramYear}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                      {stat.ProgramName}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                      {stat.DivisionName}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                      {stat.DivisionGender || 'N/A'}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                      {stat.Players}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        {/* Recent Enrollments */}
        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-xl font-bold text-gray-900 mb-4">Recent Enrollments</h2>
          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Player Name
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Program
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Division
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Order Date
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Payment Status
                  </th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {enrollments.slice(0, 20).map((enrollment, index) => (
                  <tr key={index} className="hover:bg-gray-50">
                    <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                      {enrollment.PlayerFirstName} {enrollment.PlayerLastName}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                      {enrollment.ProgramName}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                      {enrollment.DivisionName}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                      {enrollment.OrderDate
                        ? new Date(enrollment.OrderDate).toLocaleDateString()
                        : 'N/A'}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm">
                      <span
                        className={`px-2 py-1 inline-flex text-xs leading-5 font-semibold rounded-full ${
                          enrollment.OrderPaymentStatus === 'Paid'
                            ? 'bg-green-100 text-green-800'
                            : 'bg-yellow-100 text-yellow-800'
                        }`}
                      >
                        {enrollment.OrderPaymentStatus || 'Unknown'}
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        {/* Top Players by Program Enrollments */}
        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-xl font-bold text-gray-900 mb-4">Top 50 Players by Program Enrollments</h2>
          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Rank
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Player Name
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Total Programs
                  </th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {playerEnrollmentStats.map((player, index) => (
                  <tr key={player.PlayerId} className="hover:bg-gray-50">
                    <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                      {index + 1}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                      {player.PlayerFirstName} {player.PlayerLastName}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm font-bold text-primary-600">
                      {player.TotalEnrollments}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </main>
    </div>
  );
}
