<template>
  <div class="book-detail-wrapper">
    <!-- 제목과 쓰레드 작성 버튼 -->
    <header class="header">
      <h1 class="book-title">{{ book.title }}</h1>
      <button class="thread-btn" @click="goToThreadWrite">+</button>
    </header>

    <div class="backback">
      <!-- 책 정보 섹션 -->
      <section class="book-info-section">
        <img :src="book.cover" alt="book cover" class="book-cover" />
        <div class="book-details">
          <p class="subtitle">{{ book.subTitle }}</p>
          <p class="description">{{ book.description }}</p>
          <button @click="generateAudio" :disabled="isGenerating">
            {{ isGenerating ? '오디오 생성 중...' : 'AI 설명 읽어주기 생성' }}
          </button>
          <div class="audiofile" v-if="book.audio_file">
            <div class="audiio-sang">
              <span class="audio-title">AI가 들려주는</span>
              <span class="audio-booktitle">{{ book.title }}</span>
            </div>
            <audio controls :src="`http://127.0.0.1:8000${book.audio_file}`">
              <source :src="book.audio_file" type="audio/mpeg" />
              브라우저가 audio 태그를 지원하지 않습니다.
            </audio>
          </div>
          <div class="sangsae"><strong>출판사:</strong> {{ book.publisher }}</div>
          <div class="sangsae"><strong>출간일:</strong> {{ book.pub_date }}</div>
          <div class="sangsae"><strong>ISBN:</strong> {{ book.isbn }}</div>
          <div class="sangsae"><strong>고객 리뷰 평점:</strong> {{ book.customer_review_rank }}</div>
        </div>
      </section>

      <!-- 관련 스레드 -->
      <section class="thread-info-section">
        <h2>관련 스레드</h2>
      </section>

      <!-- 추천 도서 + 지도 -->
      <section class="recommend-map-wrapper" v-if="recommendations.length || mapUrl">
        <div class="recommendation-section">
          <h3>이런 책은 어때요?</h3>
          <p class="recommend-desc">AI 분석 기반 도서 추천</p>
          <div class="recommend-list">
            <div
              v-for="rec in recommendations"
              :key="rec.id"
              class="recommend-card"
              @click="goToBookDetail(rec.id)"
            >
              <img :src="rec.cover" alt="추천 도서" class="recommend-cover" />
              <p class="recommend-title">{{ rec.title }}</p>
            </div>
          </div>
        </div>

        <div class="map-section" v-if="mapUrl">
          <h3>현재 위치 주변 도서관</h3>
          <iframe
            :src="mapUrl"
            width="100%"
            height="300"
            style="border:0;"
            allowfullscreen=""
            loading="lazy"
            referrerpolicy="no-referrer-when-downgrade">
          </iframe>
        </div>
      </section>

      <!-- 작가 정보 -->
      <section class="author-info-section">
        <h2>작가 정보</h2>
        <div class="author-profile">
          <img v-if="book.author_photo" :src="book.author_photo" alt="author" class="author-photo" />
          <div>
            <p class="author-name"><strong>{{ book.author }}</strong></p>
            <p class="author-desc">{{ book.author_info }}</p>
          </div>
        </div>
      </section>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  data() {
    return {
      book: {},
      isGenerating: false,
      recommendations: [],
      userLocation: null,
      mapUrl: ''
    }
  },
  async created() {
    this.loadBookData()
  },
  mounted() {
    this.getUserLocation()
  },
  watch: {
    '$route.params.bookId'(newId, oldId) {
      if (newId !== oldId) {
        this.loadBookData()
      }
    }
  },
  methods: {
    async loadBookData() {
      const bookId = Number(this.$route.params.bookId)
      try {
        const response = await axios.get(`http://127.0.0.1:8000/api/books/${bookId}/`)
        this.book = response.data

        const recRes = await axios.get(`http://127.0.0.1:8000/api/books/${bookId}/recommendations/`)
        this.recommendations = recRes.data
      } catch (error) {
        console.error('책 정보를 불러오는 데 실패했습니다:', error)
      }
    },
    goToThreadWrite() {
      this.$router.push(`/threads/${this.book.id}/write`)
    },
    async generateAudio() {
      if (this.isGenerating) return
      this.isGenerating = true
      try {
        const response = await axios.post(`http://127.0.0.1:8000/api/books/${this.book.id}/generate-audio/`)
        this.book.audio_file = response.data.audio_file
      } catch (error) {
        alert('오디오 생성에 실패했습니다.')
        console.error(error)
      } finally {
        this.isGenerating = false
      }
    },
    goToBookDetail(bookId) {
      this.$router.push(`/books/${bookId}`)
    },
    getUserLocation() {
      if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition((pos) => {
          const lat = pos.coords.latitude
          const lng = pos.coords.longitude
          this.userLocation = { lat, lng }
          this.mapUrl = `https://www.google.com/maps?q=도서관&ll=${lat},${lng}&z=15&output=embed`
        }, () => {
          console.warn('위치 정보를 가져올 수 없습니다.')
        })
      }
    }
  }
}
</script>

<style scoped>
.book-detail-wrapper {
  max-width: 900px;
  margin: 40px auto;
  font-family: "Noto Sans KR", sans-serif;
  color: #111;
}

.backback {
  padding: 30px;
  background-color: rgb(241, 241, 241);
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
  height: 50px;
}

.book-title {
  font-size: 2rem;
  font-weight: bold;
}

.thread-btn {
  background-color: #f44;
  border: none;
  color: white;
  font-size: 1.8rem;
  width: 40px;
  height: 40px;
  border-radius: 50%;
  cursor: pointer;
  line-height: 1;
  transition: background-color 0.3s ease;
}
.thread-btn:hover {
  background-color: #d33;
}

.book-info-section {
  display: flex;
  gap: 20px;
  margin-bottom: 40px;
}

.book-cover {
  width: 160px;
  height: 240px;
  object-fit: cover;
  border-radius: 6px;
  box-shadow: 0 0 10px rgba(0,0,0,0.1);
}

.book-details {
  flex: 1;
}

.subtitle {
  font-weight: 600;
  font-size: 1.1rem;
  margin-bottom: 12px;
}

.description {
  margin-bottom: 15px;
  white-space: pre-wrap;
  line-height: 1.5;
  font-size: 15px;
}

.sangsae {
  font-size: 15px;
}

.audiio-sang {
  display: flex;
  flex-direction: column;
  text-align: center;
}
.audio-title {
  font-weight: bold;
  color: crimson;
}
.audio-booktitle {
  font-weight: bold;
  color: rgb(0, 0, 0);
}
.audiofile {
  display: flex;
  align-items: center;
  justify-content: center;
}

/* 추천 도서 + 지도 섹션 */
.recommend-map-wrapper {
  display: flex;
  flex-wrap: wrap;
  gap: 30px;
  margin-top: 40px;
  border-top: 1px solid #ccc;
  padding-top: 20px;
}

.recommendation-section {
  flex: 1;
  min-width: 300px;
}

.recommend-desc {
  color: crimson;
  margin-bottom: 15px;
}

.recommend-list {
  display: flex;
  gap: 20px;
  flex-wrap: wrap;
}

.recommend-card {
  flex: 1 0 30%;
  max-width: 30%;
  text-align: center;
  cursor: pointer;
  box-sizing: border-box;
}

.recommend-cover {
  width: 100%;
  aspect-ratio: 2/3; /* ⭐ 2:3 비율 유지 (예: 160x240) */
  object-fit: cover;
  border-radius: 8px;
  box-shadow: 0 0 5px rgba(0,0,0,0.1);
}


.recommend-title {
  margin-top: 8px;
  font-size: 14px;
  font-weight: bold;
}

.map-section {
  flex: 1;
  min-width: 300px;
}

.map-section h3 {
  font-size: 1.1rem;
  margin-bottom: 10px;
}

/* 작가 정보 */
.author-info-section {
  border-top: 1px solid #ddd;
  padding-top: 30px;
}

.author-info-section h2 {
  margin-bottom: 20px;
  font-weight: 700;
  font-size: 1.4rem;
}

.author-profile {
  display: flex;
  gap: 20px;
  align-items: flex-start;
}

.author-photo {
  width: 100px;
  height: 100px;
  border-radius: 50%;
  object-fit: cover;
  box-shadow: 0 0 5px rgba(0,0,0,0.1);
}

.author-name {
  font-size: 1.2rem;
  margin-bottom: 10px;
}

.author-desc {
  font-size: 0.9rem;
  line-height: 1.4;
  white-space: pre-wrap;
}
</style>
