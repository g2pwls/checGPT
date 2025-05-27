<template>
  <div class="main-container">
  <div class="book-detail-wrapper">
    <header class="header">
      <div class="left-header">
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
      <div class="right-header">
        <button @click="addToLibrary" class="action-btn" :class="{ 'in-library': isInLibrary }">
          {{ isInLibrary ? '서재에서 제거' : '내 서재에 추가하기' }}
        </button>
        <button @click="isThreadModalOpen = true" class="action-btn thread-write-btn">스레드 작성하기</button>
        <button @click="navigateToAI" class="action-btn ai-analysis-btn">
          <i class="fas fa-robot"></i> AI 분석 시작하기
        </button>
      </div>
    </header>

    <div class="content-wrapper">
      <!-- 왼쪽 컨텐츠 영역 -->
      <div class="left-content">
        <!-- 책 정보 섹션 -->
        <section class="book-info-section">
          <img :src="book.cover" alt="book cover" class="book-cover" />
          <div class="book-details">
            <p class="subtitle">{{ book.subTitle }}</p>
            <p class="description">{{ book.description }}</p>
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
              <div class="thread-content">
                <div class="thread-title">{{ thread.title }}</div>
                <div class="thread-info">
                  <span class="thread-writer">{{ thread.writer.username }}</span>
                  <span class="thread-stats">
                    <span class="likes">❤️ {{ thread.likes_count }}</span>
                    <span class="comments">💬 {{ thread.comments_count }}</span>
                  </span>
                </div>
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
      </div>

      <!-- 오른쪽 컨텐츠 영역 -->
      <div class="right-content">
        <!-- 작가 정보 -->
        <section class="author-info-section">
          <h2 style="margin-top: 0px;">작가 정보</h2>
          <div class="author-profile">
            <img v-if="book.author_photo" :src="book.author_photo" alt="author" class="author-photo" />
            <div>
              <p class="author-name"><strong>{{ book.author }}</strong></p>
              <p class="author-desc">{{ book.author_info }}</p>
            </div>
          </div>
        </section>

        <!-- AI 설명 읽어주기 섹션 -->
        <section class="ai-audio-section">
          <button @click="generateAudio" :disabled="isGenerating || isGenerated" class="ai-audio-btn">
            {{ buttonText }}
          </button>
          <div class="audiofile" v-if="book.audio_file">
            <div class="audiio-sang">
              <span class="audio-title">AI가 들려주는</span>
              <span class="audio-booktitle">{{ book.title }}</span>
            </div>
            <audio controls :src="`http://127.0.0.1:8000${book.audio_file}`" class="audio-player" />
          </div>
        </section>
      </div>
    </div>

    <!-- ThreadWriteModal 컴포넌트 -->
    <ThreadWriteModal
      v-if="isThreadModalOpen"
      :book="book"
      @close="isThreadModalOpen = false"
      @submit-thread="addThread"
    />
  </div>
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
      isGenerated: false,
      isThreadModalOpen: false,
      isInLibrary: false,
    }
  },
  computed: {
    buttonText() {
      if (this.isGenerating) {
        return '오디오 생성 중...'
      }
      if (this.isGenerated) {
        return 'AI 설명 읽어주기 생성 완료'
      }
      return 'AI 설명 읽어주기 생성'
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
    this.setAuthToken();
    await this.loadBookData();
    await this.loadThreads();
    await this.checkLibraryStatus();
  },
  methods: {
    setAuthToken() {
      const token = localStorage.getItem('token');
      if (token) {
        axios.defaults.headers.common['Authorization'] = `Token ${token}`;
      }
    },
    async loadBookData() {
      const bookId = this.$route.params.bookId;
      try {
        const response = await axios.get(`http://127.0.0.1:8000/api/books/${bookId}/`);
        this.book = response.data;
      } catch (error) {
        if (error.response?.status === 401) {
          this.setAuthToken();
          try {
            const retryResponse = await axios.get(`http://127.0.0.1:8000/api/books/${bookId}/`);
            this.book = retryResponse.data;
          } catch (retryError) {
            console.error('책 정보를 불러오는 데 실패했습니다:', retryError);
          }
        } else {
          console.error('책 정보를 불러오는 데 실패했습니다:', error);
        }
      }
    },
    async generateAudio() {
      if (this.isGenerating) return
      this.isGenerating = true
      try {
        const response = await axios.post(`http://127.0.0.1:8000/api/books/${this.book.id}/generate-audio/`)
        this.book.audio_file = response.data.audio_file
        this.isGenerated = true
      } catch (error) {
        alert('오디오 생성에 실패했습니다.')
        console.error(error)
      } finally {
        this.isGenerating = false
      }
    },
    async loadThreads() {
      try {
        const bookId = this.$route.params.bookId;
        const res = await axios.get(`http://127.0.0.1:8000/api/books/${bookId}/threads/`, {
          params: {
            sort_by: this.sortType
          }
        });
        this.threads = res.data;
        this.updateDisplayedThreads();
      } catch (error) {
        if (error.response?.status === 401) {
          this.setAuthToken();
          try {
            const retryResponse = await axios.get(`http://127.0.0.1:8000/api/books/${this.$route.params.bookId}/threads/`, {
              params: {
                sort_by: this.sortType
              }
            });
            this.threads = retryResponse.data;
            this.updateDisplayedThreads();
          } catch (retryError) {
            console.error('스레드 불러오기 실패:', retryError);
          }
        } else {
          console.error('스레드 불러오기 실패:', error);
        }
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
        this.isInLibrary = libraryRes.data.library.some(item => item.book.id === this.book.id)
      } catch (error) {
        if (error.response?.status === 401) {
          this.setAuthToken();
          try {
            const retryResponse = await axios.get(`http://127.0.0.1:8000/api/users/library/`);
            this.isInLibrary = retryResponse.data.some(item => item.book.id === this.book.id);
          } catch (retryError) {
            console.error('서재 상태 확인 실패:', retryError);
          }
        } else {
          console.error('서재 상태 확인 실패:', error);
        }
      }
    },
    async addToLibrary() {
      try {
        if (this.isInLibrary) {
          await axios.delete(
            `http://127.0.0.1:8000/api/books/${this.book.id}/remove-from-library/`
          );
        } else {
          await axios.post(
            `http://127.0.0.1:8000/api/books/${this.book.id}/add-to-library/`
          );
        }
        this.isInLibrary = !this.isInLibrary;
      } catch (error) {
        console.error('서재 업데이트 실패:', error)
        if (error.response?.status === 401) {
          alert('로그인이 필요합니다.')
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
        const response = await axios.post(
          `http://127.0.0.1:8000/api/books/${this.book.id}/like/`
        );
        this.book.is_liked = response.data.liked;
        this.book.likes_count = response.data.likes_count;
      } catch (error) {
        if (error.response?.status === 401) {
          this.setAuthToken();
          try {
            const retryResponse = await axios.post(
              `http://127.0.0.1:8000/api/books/${this.book.id}/like/`
            );
            this.book.is_liked = retryResponse.data.liked;
            this.book.likes_count = retryResponse.data.likes_count;
          } catch (retryError) {
            console.error('좋아요 토글 실패:', retryError);
            alert('로그인이 필요한 기능입니다.');
          }
        } else {
          console.error('좋아요 토글 실패:', error);
          if (error.response?.status === 401) {
            alert('로그인이 필요한 기능입니다.');
          }
        }
      }
    },
    goToCommunity() {
      this.$router.push(`/books/${this.book.id}/community`);
    },
    navigateToAI() {
      this.$router.push({
        name: 'ai',
        params: {
          book: JSON.stringify(this.book)
        }
      });
    }
  }
}
</script>

<style scoped>
.main-container {
  background-color: #ffffff;
}
.book-detail-wrapper {
  max-width: 1500px;
  margin: 0 auto;
  padding: 20px;
  min-height: 93.9vh;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
  padding: 12px 30px 12px 30px;
  background-color: white;
  border-radius: 0px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  border: 1px solid #dadada;
}

.left-header {
  display: flex;
  align-items: center;
  gap: 20px;
}

.book-title {
  font-size: 1.8rem;
  margin: 0;
}

.right-header {
  display: flex;
  gap: 10px;
}

.content-wrapper {
  display: flex;
  gap: 10px;
  background-color: #f5f5f5;
  padding: 10px;
  border-radius: 0px;
}

.left-content {
  flex: 1.2;
  background-color: white;
  border-radius: 0px;
  padding: 20px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.right-content {
  flex: 0.8;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.book-info-section {
  display: flex;
  gap: 30px;
  margin-bottom: 30px;
}

.book-cover {
  height: 300px;
  width: 200px;
  border-radius: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  object-fit: cover;
}

.book-details {
  flex: 1;
}

.subtitle {
  font-size: 1.2rem;
  color: #666;
  margin-bottom: 15px;
  margin-top: 0px;
}

.description {
  line-height: 1.5;
  margin-bottom: 20px;
  color: #333;
}

.sangsae {
  margin-bottom: 0px;
  color: #666;
}

.author-info-section,
.ai-audio-section {
  background-color: white;
  border-radius: 0px;
  padding: 20px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.author-profile {
  display: flex;
  gap: 20px;
  margin-top: 15px;
}

.author-photo {
  width: 120px;
  height: 120px;
  border-radius: 50%;
  object-fit: cover;
}

.author-name {
  font-size: 1.2rem;
  margin-bottom: 10px;
}

.author-desc {
  color: #666;
  line-height: 1.5;
}

.ai-audio-btn {
  width: 100%;
  padding: 15px;
  background-color: #1c1c1c;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 1.1rem;
  cursor: pointer;
  transition: background-color 0.3s;
  /* margin-bottom: 15px; */
}

.ai-audio-btn:hover {
  background-color: #ff6c6c;
}

.ai-audio-btn:disabled {
  background-color: #cccccc;
  cursor: not-allowed;
}

.audio-player {
  width: 100%;
  margin-top: 10px;
}

.audiio-sang {
  text-align: center;
  margin-bottom: 10px;
}

.audio-title {
  font-size: 0.9rem;
  color: #666;
}

.audio-booktitle {
  display: block;
  font-size: 1.1rem;
  font-weight: bold;
  color: #333;
  margin-top: 5px;
}

.thread-info-section {
  margin-top: 30px;
}

.thread-sort-tabs {
  display: flex;
  gap: 10px;
  margin-bottom: 20px;
}

.sort-tab {
  padding: 8px 16px;
  border: none;
  background-color: #f0f0f0;
  border-radius: 20px;
  cursor: pointer;
  transition: all 0.3s;
}

.sort-tab.active {
  background-color: #1c1c1c;
  color: white;
}

.thread-box {
  padding: 12px 20px;
  background-color: #f9f9f9;
  border-radius: 8px;
  margin-bottom: 10px;
  transition: all 0.3s ease;
  border: 1px solid #dedede;
}

.thread-box:hover {
  transform: translateY(-2px);
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  background-color: #f0f0f0;
}

.thread-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 20px;
}

.thread-title {
  font-size: 1.1rem;
  font-weight: 500;
  color: #333;
  flex: 1;
}

.thread-info {
  display: flex;
  align-items: center;
  gap: 20px;
  color: #666;
  white-space: nowrap;
}

.thread-writer {
  color: #2c3e50;
  font-weight: 500;
}

.thread-stats {
  display: flex;
  gap: 15px;
}

.likes, .comments {
  display: flex;
  align-items: center;
  gap: 5px;
}

.action-buttons {
  display: flex;
  gap: 1rem;
  margin-top: 0px;
}

.like-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  border: none;
  background: #f8f9fa;
  border-radius: 20px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.like-btn:hover {
  transform: scale(1.05);
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
  background: #1c1c1c;
  color: white;
  border-radius: 20px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.community-btn:hover {
  background: #45a049;
  transform: scale(1.05);
}

.action-btn {
  padding: 10px 20px;
  border: none;
  border-radius: 20px;
  background-color: #1c1c1c;
  color: white;
  cursor: pointer;
  transition: all 0.3s ease;
  font-size: 0.9rem;
}

.action-btn:hover {
  background-color: #505050;
}

.action-btn.in-library {
  background-color: #95a5a6;
}

.action-btn.in-library:hover {
  background-color: #7f8c8d;
}

.thread-write-btn {
  background-color: #1c1c1c;
}

.thread-write-btn:hover {
  background-color: #505050;
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

.ai-button {
  background-color: #e53935;
  color: white;
  border: none;
  padding: 0.8rem 1.5rem;
  border-radius: 5px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  transition: background-color 0.3s;
}

.ai-button:hover {
  background-color: #f50057;
}

.ai-button i {
  font-size: 1.1rem;
}

.ai-analysis-btn {
  background-color: #e74c3c;
  color: white;
  display: flex;
  align-items: center;
}

.ai-analysis-btn:hover {
  background-color: #ff7676;
}

.ai-analysis-btn i {
  font-size: 1.1rem;
}

@media (max-width: 1024px) {
  .header {
    flex-direction: column;
    gap: 15px;
  }

  .left-header {
    flex-direction: column;
    align-items: center;
    text-align: center;
  }

  .right-header {
    width: 100%;
    justify-content: center;
  }

  .content-wrapper {
    flex-direction: column;
  }

  .left-content,
  .right-content {
    flex: 1;
  }

  .book-info-section {
    flex-direction: column;
    align-items: center;
  }

  .book-cover {
    width: 150px;
  }
}
</style>
