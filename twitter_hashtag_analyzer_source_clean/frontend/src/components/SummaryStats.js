import React from 'react';

const SummaryStats = ({ data }) => {
  if (!data) {
    return <div className="no-data">Özet verisi bulunamadı</div>;
  }

  return (
    <div className="summary-stats">
      <div className="stats-grid">
        <div className="stat-card total-posts">
          <h3>Toplam Gönderiler</h3>
          <div className="stat-value">{data.totalTweets.toLocaleString()}</div>
          <div className="stat-breakdown">
            <div className="breakdown-item">
              <span className="label">Orijinal:</span>
              <span className="value">{data.tweetTypes.originals.toLocaleString()}</span>
              <span className="percentage">({((data.tweetTypes.originals / data.totalTweets) * 100).toFixed(2)}%)</span>
            </div>
            <div className="breakdown-item">
              <span className="label">Retweet:</span>
              <span className="value">{data.tweetTypes.retweets.toLocaleString()}</span>
              <span className="percentage">({((data.tweetTypes.retweets / data.totalTweets) * 100).toFixed(2)}%)</span>
            </div>
            <div className="breakdown-item">
              <span className="label">Yanıt:</span>
              <span className="value">{data.tweetTypes.replies.toLocaleString()}</span>
              <span className="percentage">({((data.tweetTypes.replies / data.totalTweets) * 100).toFixed(2)}%)</span>
            </div>
            <div className="breakdown-item">
              <span className="label">Medya:</span>
              <span className="value">{data.tweetTypes.media.toLocaleString()}</span>
              <span className="percentage">({((data.tweetTypes.media / data.totalTweets) * 100).toFixed(2)}%)</span>
            </div>
          </div>
        </div>

        <div className="stat-card contributors">
          <h3>Katılımcılar</h3>
          <div className="stat-value">{data.totalContributors.toLocaleString()}</div>
          <div className="stat-detail">
            <span className="label">Gönderi/Katılımcı:</span>
            <span className="value">{(data.totalTweets / data.totalContributors).toFixed(2)}</span>
          </div>
        </div>

        <div className="stat-card sentiment">
          <h3>Duygu Skoru</h3>
          <div className="stat-value">{data.sentimentScore.toFixed(2)}</div>
          <div className="stat-detail">
            <span className="label">Ölçek:</span>
            <span className="value">0-10 (10 = En Olumlu)</span>
          </div>
        </div>

        <div className="stat-card economic">
          <h3>Ekonomik Değer</h3>
          <div className="stat-value">{data.economicValue}</div>
          <div className="stat-detail">
            <span className="label">Tahmini erişim değeri</span>
          </div>
        </div>
      </div>

      <div className="summary-description">
        <h3>Hashtag Özeti</h3>
        <p>
          Bu hashtag toplam <strong>{data.totalTweets.toLocaleString()}</strong> gönderi içermektedir ve 
          <strong> {data.totalContributors.toLocaleString()}</strong> benzersiz katılımcı tarafından kullanılmıştır.
        </p>
        <p>
          Gönderilerin <strong>{((data.tweetTypes.originals / data.totalTweets) * 100).toFixed(2)}%</strong>'i orijinal içerik, 
          <strong> {((data.tweetTypes.retweets / data.totalTweets) * 100).toFixed(2)}%</strong>'i retweet ve 
          <strong> {((data.tweetTypes.replies / data.totalTweets) * 100).toFixed(2)}%</strong>'i yanıttır.
        </p>
        <p>
          Genel duygu skoru <strong>{data.sentimentScore.toFixed(2)}</strong> olarak ölçülmüştür, bu da 
          hashtag'in genel olarak <strong>{data.sentimentScore >= 5 ? 'olumlu' : 'olumsuz'}</strong> bir tona sahip olduğunu gösterir.
        </p>
      </div>
    </div>
  );
};

export default SummaryStats;
