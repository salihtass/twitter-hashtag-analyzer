import React from 'react';
import { Chart as ChartJS, CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend, Filler } from 'chart.js';
import { Line } from 'react-chartjs-2';

// Register ChartJS components
ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  Filler
);

const ActivityChart = ({ data }) => {
  if (!data || !data.timeline || data.timeline.length === 0) {
    return <div className="no-data">Aktivite verisi bulunamadı</div>;
  }

  // Prepare data for the chart
  const labels = data.timeline.map(item => {
    const date = new Date(item.timestamp);
    return date.toLocaleTimeString('tr-TR', { hour: '2-digit', minute: '2-digit' });
  });

  const chartData = {
    labels,
    datasets: [
      {
        label: 'Tweetler',
        data: data.timeline.map(item => item.tweets),
        borderColor: 'rgb(53, 162, 235)',
        backgroundColor: 'rgba(53, 162, 235, 0.5)',
        tension: 0.3,
      },
      {
        label: 'Katılımcılar',
        data: data.timeline.map(item => item.contributors),
        borderColor: 'rgb(75, 192, 192)',
        backgroundColor: 'rgba(75, 192, 192, 0.5)',
        tension: 0.3,
      },
      {
        label: 'Retweetler',
        data: data.timeline.map(item => item.retweets),
        borderColor: 'rgb(255, 99, 132)',
        backgroundColor: 'rgba(255, 99, 132, 0.5)',
        tension: 0.3,
      },
      {
        label: 'Yanıtlar',
        data: data.timeline.map(item => item.replies),
        borderColor: 'rgb(255, 159, 64)',
        backgroundColor: 'rgba(255, 159, 64, 0.5)',
        tension: 0.3,
      },
      {
        label: 'Medya',
        data: data.timeline.map(item => item.media),
        borderColor: 'rgb(153, 102, 255)',
        backgroundColor: 'rgba(153, 102, 255, 0.5)',
        tension: 0.3,
      },
    ],
  };

  const options = {
    responsive: true,
    plugins: {
      legend: {
        position: 'top',
      },
      title: {
        display: true,
        text: 'Zaman İçinde Aktivite',
      },
    },
    scales: {
      y: {
        beginAtZero: true,
      },
    },
  };

  return (
    <div className="activity-chart">
      <h3>Tweet Aktivitesi</h3>
      <div className="chart-container">
        <Line data={chartData} options={options} />
      </div>
      <div className="chart-description">
        <p>
          Bu grafik, hashtag'in zaman içindeki aktivitesini göstermektedir. 
          Tweet sayısı, katılımcı sayısı, retweet sayısı, yanıt sayısı ve medya içeren tweet sayısı 
          gibi metrikleri içerir.
        </p>
      </div>
    </div>
  );
};

export default ActivityChart;
