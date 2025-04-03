import React, { useState } from 'react';
import SummaryStats from './SummaryStats';
import ActivityChart from './ActivityChart';
import SentimentAnalysis from './SentimentAnalysis';
import TopContributors from './TopContributors';
import MapVisualization from './MapVisualization';
import SearchBar from './SearchBar';

const Dashboard = () => {
  const [activeTab, setActiveTab] = useState('summary');
  const [hashtag, setHashtag] = useState('');
  const [loading, setLoading] = useState(false);
  const [data, setData] = useState(null);
  const [error, setError] = useState(null);

  const handleSearch = async (searchedHashtag) => {
    if (!searchedHashtag) return;
    
    setLoading(true);
    setError(null);
    setHashtag(searchedHashtag);
    
    try {
      // In a real implementation, this would call the backend API
      // For now, we'll use mock data
      setTimeout(() => {
        const mockData = getMockData(searchedHashtag);
        setData(mockData);
        setLoading(false);
      }, 1500);
    } catch (err) {
      setError('Hashtag analizi yapılırken bir hata oluştu. Lütfen tekrar deneyin.');
      setLoading(false);
    }
  };

  const renderTabContent = () => {
    if (loading) {
      return <div className="loading">Hashtag analiz ediliyor...</div>;
    }

    if (error) {
      return <div className="error">{error}</div>;
    }

    if (!data) {
      return <div className="empty-state">Lütfen analiz etmek için bir hashtag girin</div>;
    }

    switch (activeTab) {
      case 'summary':
        return <SummaryStats data={data.summary} />;
      case 'activity':
        return <ActivityChart data={data.activity} />;
      case 'sentiment':
        return <SentimentAnalysis data={data.sentiment} />;
      case 'contributors':
        return <TopContributors data={data.topContributors} />;
      case 'map':
        return <MapVisualization data={data.locations} />;
      default:
        return <SummaryStats data={data.summary} />;
    }
  };

  return (
    <div className="dashboard">
      <header className="dashboard-header">
        <h1>Twitter Hashtag Analiz Aracı</h1>
        <SearchBar onSearch={handleSearch} />
      </header>

      {hashtag && data && (
        <div className="hashtag-title">
          <h2>#{hashtag}</h2>
          <span className="date-range">{data.dateRange}</span>
        </div>
      )}

      <div className="tabs">
        <button 
          className={`tab ${activeTab === 'summary' ? 'active' : ''}`}
          onClick={() => setActiveTab('summary')}
        >
          Özet
        </button>
        <button 
          className={`tab ${activeTab === 'activity' ? 'active' : ''}`}
          onClick={() => setActiveTab('activity')}
        >
          Aktivite
        </button>
        <button 
          className={`tab ${activeTab === 'sentiment' ? 'active' : ''}`}
          onClick={() => setActiveTab('sentiment')}
        >
          Duygu Analizi
        </button>
        <button 
          className={`tab ${activeTab === 'contributors' ? 'active' : ''}`}
          onClick={() => setActiveTab('contributors')}
        >
          Katılımcılar
        </button>
        <button 
          className={`tab ${activeTab === 'map' ? 'active' : ''}`}
          onClick={() => setActiveTab('map')}
        >
          Harita
        </button>
      </div>

      <div className="tab-content">
        {renderTabContent()}
      </div>
    </div>
  );
};

// Mock data function for development
const getMockData = (hashtag) => {
  return {
    summary: {
      totalTweets: 23230,
      totalContributors: 3715,
      sentimentScore: 9.91,
      economicValue: '$75,627.63',
      tweetTypes: {
        originals: 1545,
        retweets: 21685,
        replies: 493,
        media: 894
      }
    },
    activity: {
      timeline: [
        { timestamp: '2025-04-01 12:00', tweets: 12000, contributors: 1800, retweets: 10000, replies: 1200, media: 800 },
        { timestamp: '2025-04-01 13:00', tweets: 3000, contributors: 1200, retweets: 2500, replies: 300, media: 200 },
        { timestamp: '2025-04-01 14:00', tweets: 1200, contributors: 800, retweets: 1000, replies: 100, media: 100 },
        { timestamp: '2025-04-01 15:00', tweets: 1100, contributors: 750, retweets: 900, replies: 100, media: 100 },
        { timestamp: '2025-04-01 16:00', tweets: 900, contributors: 600, retweets: 750, replies: 80, media: 70 },
        { timestamp: '2025-04-01 17:00', tweets: 800, contributors: 550, retweets: 650, replies: 80, media: 70 },
        { timestamp: '2025-04-01 18:00', tweets: 700, contributors: 500, retweets: 550, replies: 80, media: 70 },
        { timestamp: '2025-04-01 19:00', tweets: 600, contributors: 450, retweets: 480, replies: 70, media: 50 },
        { timestamp: '2025-04-01 20:00', tweets: 500, contributors: 400, retweets: 400, replies: 60, media: 40 },
        { timestamp: '2025-04-01 21:00', tweets: 400, contributors: 350, retweets: 320, replies: 50, media: 30 },
        { timestamp: '2025-04-01 22:00', tweets: 300, contributors: 250, retweets: 240, replies: 40, media: 20 },
        { timestamp: '2025-04-01 23:00', tweets: 200, contributors: 150, retweets: 160, replies: 30, media: 10 },
      ]
    },
    sentiment: {
      overall: 9.91,
      distribution: {
        positive: 96,
        negative: 1,
        neutral: 3
      },
      timeline: [
        { timestamp: '2025-04-01 12:00', score: 9.8 },
        { timestamp: '2025-04-01 13:00', score: 9.9 },
        { timestamp: '2025-04-01 14:00', score: 9.7 },
        { timestamp: '2025-04-01 15:00', score: 9.8 },
        { timestamp: '2025-04-01 16:00', score: 9.9 },
        { timestamp: '2025-04-01 17:00', score: 10.0 },
        { timestamp: '2025-04-01 18:00', score: 9.9 },
        { timestamp: '2025-04-01 19:00', score: 9.8 },
        { timestamp: '2025-04-01 20:00', score: 9.9 },
        { timestamp: '2025-04-01 21:00', score: 10.0 },
        { timestamp: '2025-04-01 22:00', score: 9.9 },
        { timestamp: '2025-04-01 23:00', score: 9.8 },
      ]
    },
    topContributors: [
      { username: 'user1', displayName: 'User One', tweetCount: 359, followers: 554265, influence: 10.0 },
      { username: 'user2', displayName: 'User Two', tweetCount: 190, followers: 258110, influence: 9.5 },
      { username: 'user3', displayName: 'User Three', tweetCount: 186, followers: 228708, influence: 9.2 },
      { username: 'user4', displayName: 'User Four', tweetCount: 184, followers: 150000, influence: 8.8 },
      { username: 'user5', displayName: 'User Five', tweetCount: 177, followers: 120000, influence: 8.5 },
      { username: 'user6', displayName: 'User Six', tweetCount: 150, followers: 100000, influence: 8.2 },
      { username: 'user7', displayName: 'User Seven', tweetCount: 130, followers: 90000, influence: 7.9 },
      { username: 'user8', displayName: 'User Eight', tweetCount: 120, followers: 80000, influence: 7.6 },
      { username: 'user9', displayName: 'User Nine', tweetCount: 110, followers: 70000, influence: 7.3 },
      { username: 'user10', displayName: 'User Ten', tweetCount: 100, followers: 60000, influence: 7.0 },
    ],
    locations: [
      { location: 'İstanbul, Türkiye', latitude: 41.0082, longitude: 28.9784, userCount: 850 },
      { location: 'Ankara, Türkiye', latitude: 39.9334, longitude: 32.8597, userCount: 450 },
      { location: 'İzmir, Türkiye', latitude: 38.4237, longitude: 27.1428, userCount: 350 },
      { location: 'Bursa, Türkiye', latitude: 40.1885, longitude: 29.0610, userCount: 200 },
      { location: 'Antalya, Türkiye', latitude: 36.8969, longitude: 30.7133, userCount: 180 },
      { location: 'Adana, Türkiye', latitude: 37.0000, longitude: 35.3213, userCount: 150 },
      { location: 'Konya, Türkiye', latitude: 37.8667, longitude: 32.4833, userCount: 120 },
      { location: 'Gaziantep, Türkiye', latitude: 37.0662, longitude: 37.3833, userCount: 100 },
      { location: 'Şanlıurfa, Türkiye', latitude: 37.1591, longitude: 38.7969, userCount: 90 },
      { location: 'Kayseri, Türkiye', latitude: 38.7312, longitude: 35.4787, userCount: 80 },
      { location: 'Diyarbakır, Türkiye', latitude: 37.9144, longitude: 40.2306, userCount: 70 },
      { location: 'Mersin, Türkiye', latitude: 36.8000, longitude: 34.6333, userCount: 65 },
      { location: 'Eskişehir, Türkiye', latitude: 39.7767, longitude: 30.5206, userCount: 60 },
      { location: 'Samsun, Türkiye', latitude: 41.2867, longitude: 36.3300, userCount: 55 },
      { location: 'Denizli, Türkiye', latitude: 37.7765, longitude: 29.0864, userCount: 50 },
      { location: 'Sakarya, Türkiye', latitude: 40.7731, longitude: 30.3943, userCount: 45 },
      { location: 'Malatya, Türkiye', latitude: 38.3552, longitude: 38.3095, userCount: 40 },
      { location: 'Trabzon, Türkiye', latitude: 41.0015, longitude: 39.7178, userCount: 35 },
      { location: 'Erzurum, Türkiye', latitude: 39.9000, longitude: 41.2700, userCount: 30 },
      { location: 'Van, Türkiye', latitude: 38.4891, longitude: 43.4089, userCount: 25 },
    ],
    dateRange: '1 Nisan 2025 - 3 Nisan 2025'
  };
};

export default Dashboard;
