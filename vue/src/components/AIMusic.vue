<template>
  <div class="music-recommendation-wrapper">
    <h1 class="title">{{ book.title }} 관련 음악 추천</h1>
    
    <!-- 음악 추천 섹션 -->
    <section class="music-section">
      <div v-if="isLoading" class="section-loading">
        <div class="loading-spinner"></div>
        <p>음악 추천을 생성하는 중입니다...</p>
      </div>
      
      <div v-else-if="recommendedTracks.length > 0" class="music-grid">
        <div v-for="track in recommendedTracks" :key="track.id" 
             class="music-card"
             @click="openMusicModal(track, $event)">
          <div class="album-cover">
            <img :src="track.albumCover" :alt="track.albumName" />
          </div>
          <div class="music-info">
            <h3 class="track-title">{{ track.name }}</h3>
            <p class="artist-name">{{ track.artist }}</p>
            <p class="album-name">{{ track.albumName }}</p>
          </div>
        </div>
      </div>
      <div v-else class="no-music">
        <p>관련 음악을 찾을 수 없습니다.</p>
      </div>
    </section>

    <!-- 음악 상세 모달 -->
    <div v-if="selectedTrack" class="music-modal" @click.self="closeMusicModal">
      <div class="modal-content" :style="modalStyle">
        <button class="close-button" @click="closeMusicModal">&times;</button>
        <div class="modal-body">
          <div class="modal-album">
            <img :src="selectedTrack.albumCover" :alt="selectedTrack.albumName" class="modal-album-cover">
            <div class="modal-info">
              <h2 class="modal-title">{{ selectedTrack.name }}</h2>
              <p class="modal-artist">{{ selectedTrack.artist }}</p>
              <div class="album-details">
                <h3>앨범</h3>
                <p>{{ selectedTrack.albumName }}</p>
                
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'AIMusic',
  props: {
    book: {
      type: Object,
      required: true
    }
  },
  data() {
    return {
      recommendedTracks: [],
      isLoading: true,
      accessToken: null,
      selectedTrack: null,
      modalPosition: null
    }
  },
  computed: {
    modalStyle() {
      if (!this.modalPosition) return {}
      
      return {
        '--initial-top': `${this.modalPosition.top}px`,
        '--initial-left': `${this.modalPosition.left}px`,
        '--initial-width': `${this.modalPosition.width}px`,
        '--initial-height': `${this.modalPosition.height}px`
      }
    }
  },
  async created() {
    await this.getSpotifyToken()
    await this.getMusicRecommendations()
    this.isLoading = false
  },
  methods: {
    async getSpotifyToken() {
      try {
        const clientId = '21b8d2d1a90940faab04e31992183f98'
        const clientSecret = 'b96cb47acda642a98e901521e65d451c'
        
        const response = await axios.post('https://accounts.spotify.com/api/token', 
          'grant_type=client_credentials', {
          headers: {
            'Authorization': 'Basic ' + btoa(clientId + ':' + clientSecret),
            'Content-Type': 'application/x-www-form-urlencoded'
          }
        })
        
        this.accessToken = response.data.access_token
      } catch (error) {
        console.error('Spotify 토큰을 가져오는 데 실패했습니다:', error)
      }
    },
    async getMusicRecommendations() {
      try {
        const prompt = `다음 책의 내용을 바탕으로 관련된 음악을 6곡 추천해주세요:
제목: ${this.book.title}
작가: ${this.book.author}
줄거리: ${this.book.description}

무엇보다 중요한 부분입니다.
위의 줄거리는 단순히 참고만 하고,
직접 해당 도서의 줄거리를 찾아서 이 책의 내용과 분위기, 주제, 감정과 밀접하게 관련된 음악 3가지를 추천해 주세요.

다음 형식으로 응답해주세요:
{
  "tracks": [
    {
      "name": "노래 제목",
      "artist": "가수 이름"
    }
  ]
}
`

        const response = await axios.post('https://api.openai.com/v1/chat/completions', {
          model: "gpt-4o-mini",
          messages: [{
            role: "user",
            content: prompt
          }],
          temperature: 0.7,
          max_tokens: 500
        }, {
          headers: {
            'Authorization': `Bearer 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`,
            'Content-Type': 'application/json'
          }
        })

        const content = response.data.choices[0].message.content
        const parsedContent = JSON.parse(content)
        
        // Spotify에서 각 트랙 검색
        for (const track of parsedContent.tracks) {
          await this.searchSpotifyTrack(track)
        }
        
        this.recommendedTracks = parsedContent.tracks
      } catch (error) {
        console.error('음악 추천을 가져오는 데 실패했습니다:', error)
      }
    },
    async searchSpotifyTrack(track) {
      try {
        const query = `${track.name} ${track.artist}`
        const response = await axios.get('https://api.spotify.com/v1/search', {
          params: {
            q: query,
            type: 'track',
            limit: 1
          },
          headers: {
            'Authorization': `Bearer ${this.accessToken}`
          }
        })

        if (response.data.tracks.items.length > 0) {
          const spotifyTrack = response.data.tracks.items[0]
          // Spotify에서 가져온 정보로 업데이트
          track.id = spotifyTrack.id
          track.name = spotifyTrack.name
          track.artist = spotifyTrack.artists[0].name
          track.albumName = spotifyTrack.album.name
          track.albumCover = spotifyTrack.album.images[0].url
          
          // 앨범 ID를 저장
          track.albumId = spotifyTrack.album.id
          
          // 앨범 상세 정보 가져오기
          await this.getAlbumDetails(track)
        }
      } catch (error) {
        console.error('Spotify 트랙 검색에 실패했습니다:', error)
      }
    },
    async getAlbumDetails(track) {
      try {
        const response = await axios.get(`https://api.spotify.com/v1/albums/${track.albumId}`, {
          headers: {
            'Authorization': `Bearer ${this.accessToken}`
          }
        })
        
        if (response.data) {
          track.albumDescription = response.data.description || '앨범 설명이 없습니다.'
        }
      } catch (error) {
        console.error('앨범 상세 정보를 가져오는 데 실패했습니다:', error)
        track.albumDescription = '앨범 설명을 가져올 수 없습니다.'
      }
    },
    openMusicModal(track, event) {
      this.selectedTrack = track
      document.body.style.overflow = 'hidden'
      
      const card = event.currentTarget
      const rect = card.getBoundingClientRect()
      this.modalPosition = {
        top: rect.top,
        left: rect.left,
        width: rect.width,
        height: rect.height
      }
    },
    closeMusicModal() {
      this.selectedTrack = null
      document.body.style.overflow = 'auto'
    }
  }
}
</script>

<style scoped>
.music-recommendation-wrapper {
  box-sizing: border-box;
  margin-top: 30px;
  background-color: #ffffff;
  border-radius: 15px;
  padding: 25px;
  border: 1px solid #ddd;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.05);
  width: 100%;
}

.section-loading {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 40px;
  background-color: #f8f8f8; /* 밝은 회색 배경 */
  border-radius: 8px; /* 둥근 모서리 */
  margin: 20px 0;
  border: 1px solid #eee;
}

.loading-spinner {
  width: 40px;
  height: 40px;
  border: 4px solid #f3f3f3;
  border-top: 4px solid #3498db;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: 15px;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.title {
  font-size: 1.5rem; /* 폰트 크기 조정 */
  color: #333; /* 어두운 글자색 */
  margin-bottom: 20px; /* 마진 조정 */
  text-align: center;
  padding-bottom: 10px;
  border-bottom: 1px solid #eee; /* 하단 테두리 */
  font-weight: 400;
}

.music-section {
  margin-bottom: 0; /* 마진 제거 */
}

.music-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(150px, 1fr)); /* 그리드 조정 */
  gap: 20px;
  margin-top: 20px;
}

.music-card {
  background-color: #f9f9f9; /* 밝은 배경 */
  border-radius: 8px; /* 둥근 모서리 */
  overflow: hidden;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.03); /* 가벼운 그림자 */
  transition: all 0.2s ease; /* 트랜지션 조정 */
  cursor: pointer;
  border: 1px solid #eee;
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  padding: 15px;
}

.music-card:hover {
  transform: translateY(-3px); /* 호버 효과 */
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1); /* 호버 그림자 */
}

.album-cover {
  width: 120px; /* 앨범 커버 크기 */
  height: 120px;
  margin-bottom: 10px;
  border-radius: 4px;
  border: 1px solid #ddd;
  overflow: hidden;
}

.album-cover img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.music-info {
  flex-grow: 1;
}

.track-title {
  font-size: 1rem; /* 폰트 크기 조정 */
  font-weight: bold;
  color: #333;
  margin-bottom: 5px;
  word-break: keep-all;
}

.artist-name {
  font-size: 0.9rem; /* 폰트 크기 조정 */
  color: #777;
  margin-bottom: 5px;
}

.album-name {
  font-size: 0.85rem; /* 폰트 크기 조정 */
  color: #555;
}

.no-music {
  text-align: center;
  padding: 40px;
  background-color: #ffffff; /* 흰색 배경 */
  border-radius: 8px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.05);
  border: 1px solid #ddd;
  color: #777;
}

/* 음악 상세 모달 스타일 */
.music-modal {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.7); /* 더 어두운 오버레이 */
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 2000; /* AIView의 모달보다 위에 표시 */
  animation: fadeIn 0.3s ease;
}

.modal-content {
  background-color: #ffffff; /* 흰색 배경 */
  padding: 30px;
  border-radius: 8px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3); /* 그림자 강화 */
  max-width: 600px; /* 모달 너비 조정 */
  width: 90%;
  position: relative;
  animation: scaleIn 0.3s ease;
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

@keyframes scaleIn {
  from { transform: scale(0.9); opacity: 0; }
  to { transform: scale(1); opacity: 1; }
}

.close-button {
  position: absolute;
  top: 10px;
  right: 10px;
  font-size: 1.8rem; /* 폰트 크기 증가 */
  border: none;
  background: none;
  cursor: pointer;
  color: #777; /* 무채색 */
  transition: color 0.2s ease;
}

.close-button:hover {
  color: #333; /* 호버 색상 */
}

.modal-body {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.modal-album {
  display: flex;
  gap: 20px;
  align-items: center;
}

.modal-album-cover {
  width: 150px; /* 모달 앨범 커버 크기 */
  height: 150px;
  object-fit: cover;
  border-radius: 4px;
  border: 1px solid #ddd;
}

.modal-info {
  flex-grow: 1;
}

.modal-title {
  font-size: 1.5rem; /* 모달 제목 폰트 크기 */
  font-weight: bold;
  color: #333;
  margin-bottom: 5px;
}

.modal-artist {
  font-size: 1.1rem; /* 모달 아티스트 폰트 크기 */
  color: #777;
  margin-bottom: 15px;
}

.album-details h3 {
  font-size: 1.1rem; /* 앨범 상세 제목 폰트 크기 */
  font-weight: bold;
  color: #333;
  margin-bottom: 5px;
}

.album-details p {
  font-size: 1rem;
  color: #555;
  line-height: 1.4;
}

@media (max-width: 768px) {
  .music-grid {
    grid-template-columns: repeat(auto-fill, minmax(120px, 1fr)); /* 모바일 그리드 */
    gap: 15px;
  }

  .music-card {
    padding: 10px;
  }

  .album-cover {
    width: 80px;
    height: 80px;
  }

  .track-title {
    font-size: 0.9rem;
  }

  .artist-name,
  .album-name {
    font-size: 0.8rem;
  }

  .modal-content {
    padding: 20px;
  }

  .modal-album {
    flex-direction: column;
    align-items: center;
    text-align: center;
  }

  .modal-album-cover {
    width: 100px;
    height: 100px;
  }

  .modal-title {
    font-size: 1.3rem;
  }

  .modal-artist {
    font-size: 1rem;
  }

  .album-details h3,
  .album-details p {
    font-size: 0.9rem;
  }
}
</style>