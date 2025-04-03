import React from 'react';

const TopContributors = ({ data }) => {
  if (!data || data.length === 0) {
    return <div className="no-data">Katılımcı verisi bulunamadı</div>;
  }

  return (
    <div className="top-contributors">
      <h3>En Aktif Katılımcılar</h3>
      
      <div className="contributors-table-container">
        <table className="contributors-table">
          <thead>
            <tr>
              <th>Sıra</th>
              <th>Kullanıcı</th>
              <th>Tweet Sayısı</th>
              <th>Takipçi Sayısı</th>
              <th>Etki Puanı</th>
            </tr>
          </thead>
          <tbody>
            {data.map((contributor, index) => (
              <tr key={contributor.username}>
                <td>{index + 1}</td>
                <td className="user-cell">
                  <div className="user-info">
                    <span className="username">@{contributor.username}</span>
                    <span className="display-name">{contributor.displayName}</span>
                  </div>
                </td>
                <td>{contributor.tweetCount.toLocaleString()}</td>
                <td>{contributor.followers.toLocaleString()}</td>
                <td>
                  <div className="influence-score">
                    <div 
                      className="influence-bar" 
                      style={{ width: `${contributor.influence * 10}%` }}
                    ></div>
                    <span className="influence-value">{contributor.influence.toFixed(1)}</span>
                  </div>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <div className="contributors-explanation">
        <h4>Etki Puanı Nedir?</h4>
        <p>
          Etki puanı, bir kullanıcının hashtag içindeki etkisini ölçen bileşik bir skorudur. 
          Bu puan, kullanıcının tweet sayısı, takipçi sayısı, retweet ve beğeni oranları gibi 
          faktörlere dayanarak hesaplanır. 0-10 arasında bir ölçekte ifade edilir, burada 10 
          en yüksek etkiyi temsil eder.
        </p>
      </div>
    </div>
  );
};

export default TopContributors;
