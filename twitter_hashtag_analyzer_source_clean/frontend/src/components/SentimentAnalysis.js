import React from 'react';
import { Chart as ChartJS, ArcElement, Tooltip, Legend } from 'chart.js';
import { Pie } from 'react-chartjs-2';

// Register ChartJS components
ChartJS.register(ArcElement, Tooltip, Legend);

const SentimentAnalysis = ({ data }) => {
  if (!data) {
    return <div className="no-data">Duygu analizi verisi bulunamadı</div>;
  }

  // Prepare data for the sentiment distribution pie chart
  const distributionData = {
    labels: ['Olumlu', 'Olumsuz', 'Nötr'],
    datasets: [
      {
        data: [
          data.distribution.positive || 0,
          data.distribution.negative || 0,
          data.distribution.neutral || 0
        ],
        backgroundColor: [
          'rgba(75, 192, 192, 0.6)',
          'rgba(255, 99, 132, 0.6)',
          'rgba(201, 203, 207, 0.6)'
        ],
        borderColor: [
          'rgb(75, 192, 192)',
          'rgb(255, 99, 132)',
          'rgb(201, 203, 207)'
        ],
        borderWidth: 1,
      },
    ],
  };

  // Prepare data for the sentiment timeline chart
  const timelineLabels = data.timeline.map(item => {
    const date = new Date(item.timestamp);
    return date.toLocaleTimeString('tr-TR', { hour: '2-digit', minute: '2-digit' });
  });

  const timelineData = {
    labels: timelineLabels,
    datasets: [
      {
        label: 'Duygu Skoru',
        data: data.timeline.map(item => item.score),
        borderColor: 'rgb(75, 192, 192)',
        backgroundColor: 'rgba(75, 192, 192, 0.5)',
        tension: 0.3,
      }
    ],
  };

  const timelineOptions = {
    responsive: true,
    plugins: {
      legend: {
        position: 'top',
      },
      title: {
        display: true,
        text: 'Zaman İçinde Duygu Analizi',
      },
    },
    scales: {
      y: {
        min: 0,
        max: 10,
      },
    },
  };

  // Function to get sentiment description based on score
  const getSentimentDescription = (score) => {
    if (score >= 9) return 'Çok Olumlu';
    if (score >= 7) return 'Olumlu';
    if (score >= 5) return 'Hafif Olumlu';
    if (score >= 3) return 'Nötr';
    if (score >= 1) return 'Hafif Olumsuz';
    if (score >= 0) return 'Olumsuz';
    return 'Çok Olumsuz';
  };

  return (
    <div className="sentiment-analysis">
      <div className="sentiment-overview">
        <h3>Genel Duygu Analizi</h3>
        <div className="sentiment-score">
          <div className="score-value">{data.overall.toFixed(2)}</div>
          <div className="score-label">{getSentimentDescription(data.overall)}</div>
        </div>
      </div>

      <div className="sentiment-distribution">
        <h3>Duygu Dağılımı</h3>
        <div className="chart-container" style={{ maxWidth: '400px', margin: '0 auto' }}>
          <Pie data={distributionData} />
        </div>
        <div className="distribution-stats">
          <div className="stat">
            <span className="label">Olumlu:</span>
            <span className="value">{data.distribution.positive}%</span>
          </div>
          <div className="stat">
            <span className="label">Olumsuz:</span>
            <span className="value">{data.distribution.negative}%</span>
          </div>
          <div className="stat">
            <span className="label">Nötr:</span>
            <span className="value">{data.distribution.neutral}%</span>
          </div>
        </div>
      </div>

      <div className="sentiment-timeline">
        <h3>Zaman İçinde Duygu Değişimi</h3>
        <div className="chart-container">
          <Line 
            data={timelineData} 
            options={timelineOptions} 
          />
        </div>
      </div>

      <div className="sentiment-explanation">
        <h3>Duygu Analizi Nedir?</h3>
        <p>
          Duygu analizi, tweetlerin içeriğini analiz ederek olumlu, olumsuz veya nötr olarak sınıflandıran 
          doğal dil işleme tekniğidir. 0-10 arasında bir skor kullanılır, burada 10 en olumlu duyguyu temsil eder.
        </p>
        <p>
          Bu analiz, bir hashtag etrafındaki genel duygu durumunu anlamanıza ve zaman içinde nasıl değiştiğini 
          görmenize yardımcı olur.
        </p>
      </div>
    </div>
  );
};

export default SentimentAnalysis;
