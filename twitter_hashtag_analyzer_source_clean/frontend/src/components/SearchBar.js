import React, { useState } from 'react';

const SearchBar = ({ onSearch }) => {
  const [hashtag, setHashtag] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = (e) => {
    e.preventDefault();
    
    if (!hashtag.trim()) return;
    
    // Remove # if present
    const cleanHashtag = hashtag.trim().startsWith('#') 
      ? hashtag.trim().substring(1) 
      : hashtag.trim();
    
    setIsLoading(true);
    
    // Call the parent's onSearch function
    onSearch(cleanHashtag);
    
    // Reset loading state after a short delay
    setTimeout(() => {
      setIsLoading(false);
    }, 1500);
  };

  return (
    <div className="search-bar">
      <form onSubmit={handleSubmit}>
        <div className="search-input-container">
          <input
            type="text"
            value={hashtag}
            onChange={(e) => setHashtag(e.target.value)}
            placeholder="Hashtag girin (örn: TürkiyedeKadınOlmak)"
            disabled={isLoading}
            className="search-input"
          />
          <button 
            type="submit" 
            disabled={isLoading || !hashtag.trim()}
            className="search-button"
          >
            {isLoading ? 'Analiz Ediliyor...' : 'Analiz Et'}
          </button>
        </div>
        <div className="search-help">
          <small>
            Analiz etmek istediğiniz Twitter hashtag'ini girin. # işareti opsiyoneldir.
          </small>
        </div>
      </form>
    </div>
  );
};

export default SearchBar;
