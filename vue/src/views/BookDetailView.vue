<template>
  <div class="book-detail-wrapper">
    <header class="header">
      <div class="title-section">
        <h1 class="book-title">{{ book.title }}</h1>
        <div class="action-buttons">
          <button 
            @click="toggleLike" 
            class="like-btn"
            :class="{ 'liked': book.is_liked }"
          >
            <span class="heart-icon">{{ book.is_liked ? '❤️' : '🤍' }}</span>
            <span class="likes-count">{{ book.likes_count }}</span>
          </button>
          <button 
            v-if="book.likes_count >= 2"
            @click="goToCommunity" 
            class="community-btn"
          >
            이야기마당
          </button>
        </div>
      </div>
      <div class="actions">
        <button @click="addToLibrary" class="action-btn" :class="{ 'in-library': isInLibrary }">
          {{ isInLibrary ? '서재에서 제거' : '내 서재에 추가하기' }}
        </button>
        <button @click="isThreadModalOpen = true" class="action-btn">스레드 작성하기</button>
      </div>
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
            <audio controls :src="`http://127.0.0.1:8000${book.audio_file}`" />
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
        <div v-if="threads.length === 0">등록된 스레드가 없습니다.</div>
        <div v-else>
          <div class="thread-sort-tabs">
            <button 
              @click="sortType = 'latest'" 
              :class="{ active: sortType === 'latest' }"
              class="sort-tab"
            >
              최신순
            </button>
            <button 
              @click="sortType = 'likes'" 
              :class="{ active: sortType === 'likes' }"
              class="sort-tab"
            >
              좋아요순
            </button>
            <button 
              @click="sortType = 'comments'" 
              :class="{ active: sortType === 'comments' }"
              class="sort-tab"
            >
              댓글순
            </button>
          </div>
          <div
            v-for="thread in displayedThreads"
            :key="thread.id"
            class="thread-box"
            @click="goToThreadDetail(thread.id)"
            style="cursor: pointer;"
          >
            <div class="thread-text">
              <p class="title"><strong>{{ thread.title }}</strong></p>
              <p class="subtitle">- by {{ thread.writer.username }}</p>
            </div>
            <div class="meta">
              ❤️ {{ thread.likes_count }} ・ 💬 {{ thread.comments_count }}
            </div>
          </div>
          <button 
            v-if="threads.length > 5"
            @click="toggleThreads" 
            class="toggle-btn"
          >
            {{ showAllThreads ? '접기' : '더보기' }}
            <span class="toggle-icon">{{ showAllThreads ? '▲' : '▼' }}</span>
          </button>
        </div>
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
          <h3>이 책을 읽으면 좋은 장소</h3>
          <p class="recommend-place" v-if="recommendedPlace">{{ recommendedPlace }}</p>
          <iframe :src="mapUrl" width="100%" height="300" style="border:0;" loading="lazy"></iframe>
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

    <!-- 🟡 ThreadWriteModal 컴포넌트 -->
    <ThreadWriteModal
      v-if="isThreadModalOpen"
      :book="book"
      @close="isThreadModalOpen = false"
      @submit-thread="addThread"
    />
  </div>
</template>

<script>
import axios from 'axios'
import ThreadWriteModal from '@/components/ThreadWriteModal.vue'

export default {
  components: { ThreadWriteModal },
  data() {
    return {
      book: {},
      threads: [],
      displayedThreads: [],
      showAllThreads: false,
      sortType: 'latest',
      isGenerating: false,
      recommendations: [],
      recommendedPlace: '',
      mapUrl: '',
      isThreadModalOpen: false,
      isInLibrary: false,
    }
  },
  watch: {
    '$route.params.bookId': {
      handler: async function() {
        await this.loadBookData();
        await this.loadThreads();
        await this.checkLibraryStatus();
      },
    },
    sortType() {
      this.loadThreads()
    }
  },
  async created() {
    await this.loadBookData();
    await this.loadThreads();
    await this.checkLibraryStatus();
    await this.getRecommendedPlace();
  },
  mounted() {
    this.getUserLocation();
  },
  methods: {
    async loadBookData() {
      const bookId = this.$route.params.bookId;
      try {
        const token = localStorage.getItem('token');
        const response = await axios.get(`http://127.0.0.1:8000/api/books/${bookId}/`, {
          headers: {
            Authorization: `Token ${token}`
          }
        });
        this.book = response.data;

        const recRes = await axios.get(`http://127.0.0.1:8000/api/books/${bookId}/recommendations/`, {
          headers: {
            Authorization: `Token ${token}`
          }
        });
        this.recommendations = recRes.data;
      } catch (error) {
        console.error('책 정보를 불러오는 데 실패했습니다:', error);
      }
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
    async loadThreads() {
      try {
        const bookId = this.$route.params.bookId
        const res = await axios.get(`http://127.0.0.1:8000/api/books/${bookId}/threads/`, {
          params: {
            sort_by: this.sortType
          }
        })
        this.threads = res.data
        this.updateDisplayedThreads()
      } catch (error) {
        console.error('스레드 불러오기 실패:', error)
      }
    },
    updateDisplayedThreads() {
      this.displayedThreads = this.showAllThreads 
        ? this.threads 
        : this.threads.slice(0, 5)
    },
    toggleThreads() {
      this.showAllThreads = !this.showAllThreads;
      this.updateDisplayedThreads();
    },
    addThread(newThread) {
      this.threads.unshift(newThread)
      this.updateDisplayedThreads()
    },
    goToBookDetail(bookId) {
      this.$router.push(`/books/${bookId}`);
    },
    goToThreadDetail(threadId) {
      this.$router.push(`/threads/${threadId}`)
    },
    getUserLocation() {
      if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition((pos) => {
          const lat = pos.coords.latitude
          const lng = pos.coords.longitude
          this.mapUrl = `https://www.google.com/maps?q=도서관&ll=${lat},${lng}&z=15&output=embed`
        })
      }
    },
    async checkLibraryStatus() {
      try {
        const token = localStorage.getItem('token')
        const libraryRes = await axios.get(
          'http://127.0.0.1:8000/api/users/library/',
          {
            headers: {
              Authorization: `Token ${token}`
            }
          }
        )
        this.isInLibrary = libraryRes.data.some(item => item.book.id === this.book.id)
      } catch (error) {
        console.error('서재 상태 확인 실패:', error)
      }
    },
    async addToLibrary() {
      try {
        const token = localStorage.getItem('token')
        if (!token) {
          alert('로그인이 필요합니다.')
          return
        }

        if (this.isInLibrary) {
          await axios.delete(
            `http://127.0.0.1:8000/api/books/${this.book.id}/remove-from-library/`,
            {
              headers: {
                Authorization: `Token ${token}`
              }
            }
          )
        } else {
          await axios.post(
            `http://127.0.0.1:8000/api/books/${this.book.id}/add-to-library/`,
            {},
            {
              headers: {
                Authorization: `Token ${token}`
              }
            }
          )
        }
        this.isInLibrary = !this.isInLibrary
      } catch (error) {
        console.error('서재 업데이트 실패:', error)
        if (error.response?.status === 400) {
          alert('이미 서재에 추가된 책입니다.')
        } else {
          alert('서재 업데이트에 실패했습니다.')
        }
      }
    },
    async getRecommendedPlace() {
      try {
        const prompt = `다음 책의 실제 내용에서 가장 중요한 장면이 일어나는 구체적인 장소 하나만 알려주세요:
제목: ${this.book.title}
작가: ${this.book.author}
줄거리: ${this.book.description}

다음 조건을 반드시 지켜주세요:
1. 책의 내용에서 실제로 언급된 구체적인 장소만 알려주세요
2. 작가의 이름이나 책 제목과 관련된 일반적인 장소는 피해주세요 (예: 작가가 '한강'이라고 무조건 '한강'을 추천하지 말 것)
3. 장소는 최대한 구체적으로 알려주세요 (예: '서울'보다는 '서울 광화문 광장' 처럼)
4. 장소 이름만 알려주세요. 설명은 필요 없습니다.`;
        
        const response = await axios.post('https://api.openai.com/v1/chat/completions', {
          model: "gpt-3.5-turbo",
          messages: [{
            role: "user",
            content: prompt
          }],
          temperature: 0.7,
          max_tokens: 100
        }, {
          headers: {
            'Authorization': `Bearer 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`,
            'Content-Type': 'application/json'
          }
        });

        // GPT 응답에서 장소 추출
        const content = response.data.choices[0].message.content;
        const place = this.extractPlace(content);
        if (place) {
          this.recommendedPlace = place;
          this.updateMapUrl(place);
        }
      } catch (error) {
        console.error('장소 추천 실패:', error);
      }
    },
    extractPlace(content) {
      // 불필요한 설명이나 부가 정보를 제거하고 장소명만 추출
      const cleanedContent = content
        .replace(/^[^가-힣a-zA-Z\d]*/, '') // 시작 부분의 특수문자 제거
        .replace(/[.!?][^가-힣a-zA-Z\d]*$/, '') // 끝 부분의 특수문자와 마침표 제거
        .replace(/^장소[:：]\s*/, '') // "장소:" 같은 텍스트 제거
        .trim();
      
      return cleanedContent;
    },
    updateMapUrl(place) {
      this.mapUrl = `https://www.google.com/maps?q=${encodeURIComponent(place)}&output=embed`;
    },
    async toggleLike() {
      try {
        const token = localStorage.getItem('token');
        if (!token) {
          alert('로그인이 필요한 기능입니다.');
          return;
        }
        
        const response = await axios.post(
          `http://127.0.0.1:8000/api/books/${this.book.id}/like/`,
          {},
          {
            headers: {
              Authorization: `Token ${token}`
            }
          }
        );
        this.book.is_liked = response.data.liked;
        this.book.likes_count = response.data.likes_count;
      } catch (error) {
        console.error('좋아요 토글 실패:', error);
        if (error.response?.status === 401) {
          alert('로그인이 필요한 기능입니다.');
        }
      }
    },
    goToCommunity() {
      this.$router.push(`/books/${this.book.id}/community`);
    },
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
  margin-bottom: 20px;
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
  font-size: 14px;
  width: 120px;
  height: 30px;
  border-radius: 5px;
  cursor: pointer;
  line-height: 1;
  transition: background-color 0.3s ease;
}
.thread-btn:hover {
  background-color: #d33;
}

.thread-box {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: #fff;
  border: 1px solid #cecece;
  border-radius: 5px;
  padding: 12px 16px;
  margin-bottom: 10px;
  height: 30px;
}

.thread-text {
  display: flex;
  flex-direction: row;
  align-items: center;
}

.thread-text .title {
  font-size: 15px;
  margin: 0;
  color: #222;
}

.thread-text .subtitle {
  font-size: 13px;
  color: #888;
}

.meta {
  font-size: 13px;
  color: #999;
  white-space: nowrap;
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
  margin-top: 10px;
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

.actions {
  display: flex;
  gap: 10px;
  margin-top: 20px;
}

.action-btn {
  padding: 10px 20px;
  border: none;
  border-radius: 20px;
  background-color: #e74c3c;
  color: white;
  cursor: pointer;
  transition: all 0.3s ease;
}

.action-btn:hover {
  background-color: #c0392b;
}

.action-btn.in-library {
  background-color: #95a5a6;
}

.action-btn.in-library:hover {
  background-color: #7f8c8d;
}

.show-more-btn {
  background-color: #3498db;
  border: none;
  color: white;
  padding: 10px 20px;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s ease;
  margin-top: 10px;
}

.show-more-btn:hover {
  background-color: #2980b9;
}

.thread-sort-tabs {
  display: flex;
  gap: 10px;
  margin-bottom: 15px;
}

.sort-tab {
  padding: 8px 16px;
  border: none;
  border-radius: 20px;
  background-color: #f5f5f5;
  color: #666;
  cursor: pointer;
  transition: all 0.3s ease;
  font-size: 14px;
}

.sort-tab:hover {
  background-color: #e0e0e0;
}

.sort-tab.active {
  background-color: #3498db;
  color: white;
}

.toggle-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 5px;
  width: 100%;
  padding: 10px;
  border: none;
  border-radius: 5px;
  background-color: #3498db;
  color: white;
  cursor: pointer;
  transition: all 0.3s ease;
  margin-top: 10px;
  font-size: 14px;
}

.toggle-btn:hover {
  background-color: #2980b9;
}

.toggle-icon {
  font-size: 12px;
  transition: transform 0.3s ease;
}

.recommend-place {
  margin: 10px 0;
  padding: 10px;
  background-color: #f8f9fa;
  border-radius: 4px;
  font-size: 0.9rem;
  color: #2c3e50;
}

.title-section {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.action-buttons {
  display: flex;
  gap: 1rem;
  align-items: center;
}

.like-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  border: none;
  background: white;
  border-radius: 20px;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 2px 5px rgba(0,0,0,0.1);
}

.like-btn:hover {
  transform: scale(1.05);
}

.heart-icon {
  font-size: 1.2rem;
}

.likes-count {
  font-size: 0.9rem;
  font-weight: bold;
  color: #666;
}

.like-btn.liked {
  background: #ffebee;
}

.like-btn.liked .likes-count {
  color: #e53935;
}

.community-btn {
  padding: 0.5rem 1rem;
  border: none;
  background: #4CAF50;
  color: white;
  border-radius: 20px;
  cursor: pointer;
  transition: all 0.3s ease;
  font-weight: bold;
  box-shadow: 0 2px 5px rgba(0,0,0,0.1);
}

.community-btn:hover {
  background: #45a049;
  transform: scale(1.05);
}
</style>
