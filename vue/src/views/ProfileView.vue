<template>
  <div class="profile-container">
    <div class="content-wrapper">
      <!-- Left Sidebar -->
      <div class="left-sidebar">
        <div class="profile-box">
          <img 
            :src="getProfileImageUrl(user.profile_image)" 
            alt="프로필 사진" 
            class="profile-image"
            @error="handleImageError"
          />
          <h2 class="profile-name">{{ user.name }}</h2>
          <p class="profile-username">@{{ user.username }}</p>
          <div class="follow-stats">
            <div class="stat">
              <span class="stat-value">{{ user.followers_count || 0 }}</span>
              <span class="stat-label">팔로워</span>
            </div>
            <div class="stat">
              <span class="stat-value">{{ user.following_count || 0 }}</span>
              <span class="stat-label">팔로잉</span>
            </div>
          </div>
          <button 
            v-if="!isOwnProfile" 
            @click="toggleFollow" 
            :class="['follow-button', { 'following': user.is_following }]"
          >
            {{ user.is_following ? '팔로우 취소' : '+ 팔로우' }}
          </button>
        </div>
      </div>

      <!-- Right Content -->
      <div class="right-box">
        <div class="tabs">
          <button 
            @click="activeTab = 'library'" 
            :class="['tab-button', { active: activeTab === 'library' }]"
          >
            {{ user.name }}님의 서재
          </button>
          <button 
            @click="activeTab = 'threads'" 
            :class="['tab-button', { active: activeTab === 'threads' }]"
          >
            {{ user.name }}님의 스레드
          </button>
        </div>

        <div class="tab-content">
          <!-- Library Tab -->
          <div v-if="activeTab === 'library'" class="library-content">
            <div v-if="isOwnProfile" class="library-actions">
              <button class="edit-btn" @click="openLibraryEdit">
                대표 도서 관리
              </button>
            </div>

            <!-- Top Books Section -->
            <div v-if="topBooks.length > 0" class="top-books-section">
              <h3 class="section-title">대표 도서</h3>
              <div class="top-books-grid">
                <div v-for="topBook in topBooks" :key="topBook.id" class="top-book-item" @click="goToBook(topBook.book.id)">
                  <div class="rank-badge">{{ topBook.rank }}순위</div>
                  <div class="book-cover-container">
                    <img :src="topBook.book.cover" :alt="topBook.book.title" class="book-cover">
                  </div>
                  <h3 class="book-title">{{ topBook.book.title }}</h3>
                  <p class="book-author">{{ topBook.book.author }}</p>
                </div>
              </div>
            </div>

            <!-- Top Genres Section -->
            <div v-if="topGenres.length > 0" class="top-genres-section">
              <h3 class="section-title">선호 장르</h3>
              <div class="top-genres-grid">
                <div v-for="(genre, index) in topGenres" :key="genre.id" class="genre-item">
                  <div class="rank-badge">{{ index + 1 }}순위</div>
                  <h4 class="genre-name">{{ genre.name }}</h4>
                  <p class="genre-count">{{ genre.count }}권</p>
                </div>
              </div>
            </div>

            <div v-if="library.length === 0" class="empty-state">
              <p>서재에 추가된 책이 없습니다.</p>
            </div>
            <div v-else class="library-grid">
              <div v-for="item in library" :key="item.id" class="library-item" @click="goToBook(item.book.id)">
                <div class="book-cover-container">
                  <img :src="item.book.cover" :alt="item.book.title" class="book-cover">
                </div>
                <h3 class="book-title">{{ item.book.title }}</h3>
                <p class="book-author">{{ item.book.author }}</p>
              </div>
            </div>
          </div>

          <!-- Threads Tab -->
          <div v-if="activeTab === 'threads'" class="threads-content">
            <div v-if="threads.length === 0" class="empty-state">
              <p>작성한 스레드가 없습니다.</p>
            </div>
            <div v-else class="threads-list">
              <div v-for="thread in threads" :key="thread.id" class="thread-item" @click="goToThread(thread.id)">
                <div class="thread-header">
                  <div class="book-info">
                    <img 
                      :src="thread.book.cover" 
                      :alt="thread.book.title" 
                      class="book-cover"
                      @error="handleImageError"
                    />
                    <span class="book-title">{{ thread.book.title }}</span>
                    <div class="book-details">
                      <div class="thread-meta">
                        <span class="author">by {{ thread.writer.username }}</span>
                        <span class="date">{{ formatDate(thread.read_date) }}</span>
                      </div>
                    </div>
                  </div>
                </div>
                <div class="thread-body">
                  <h3 class="thread-title">{{ thread.title }}</h3>
                  <p class="thread-content">{{ thread.content }}</p>
                </div>
                <div class="thread-footer">
                  <div class="interactions">
                    <span>❤️ {{ thread.likes_count }}</span>
                    <span>💬 {{ thread.comments_count }}</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Library Edit Modal -->
    <div v-if="showLibraryEdit" class="modal-overlay">
      <div class="modal-content">
        <LibraryEdit 
          :library="library"
          @close="closeLibraryEdit"
          @update="updateLibrary"
        />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import axios from 'axios'
import LibraryEdit from '@/components/LibraryEdit.vue'

const route = useRoute()
const router = useRouter()
const user = ref({})
const threads = ref([])
const library = ref([])
const topBooks = ref([])
const topGenres = ref([])
const isFollowing = ref(false)
const activeTab = ref('library')
const showLibraryEdit = ref(false)

// Check if this is the user's own profile
const isOwnProfile = computed(() => {
  const currentUserId = localStorage.getItem('userId')
  return !route.params.userId || route.params.userId === currentUserId
})

const getProfileImageUrl = (imagePath) => {
  if (!imagePath) return '/default-profile.png'
  if (imagePath.startsWith('http')) return imagePath
  return `http://127.0.0.1:8000${imagePath}`
}

const formatDate = (dateString) => {
  if (!dateString) return ''
  try {
    const date = new Date(dateString)
    if (isNaN(date.getTime())) return ''
    
    const year = date.getFullYear()
    const month = String(date.getMonth() + 1).padStart(2, '0')
    const day = String(date.getDate()).padStart(2, '0')
    
    return `${year}/${month}/${day}`
  } catch (error) {
    console.error('Date formatting error:', error)
    return ''
  }
}

const loadProfileData = async () => {
  try {
    const token = localStorage.getItem('token')
    if (!token) {
      router.push('/login')
      return
    }

    const userId = route.params.userId
    console.log('Current route userId:', userId)
    
    const endpoint = `http://127.0.0.1:8000/accounts/api/users/${userId}/profile/`
    
    console.log('Loading profile from:', endpoint)
    const res = await axios.get(endpoint, {
      headers: {
        Authorization: `Token ${token}`
      }
    })
    console.log('Profile response:', res.data)
    
    if (res.data) {
      user.value = res.data
      console.log('User value after setting:', user.value)
      isFollowing.value = user.value.is_following

      if (user.value.id) {
        console.log('User ID found:', user.value.id)
        try {
          // Load user's library
          const libraryEndpoint = `http://127.0.0.1:8000/api/users/${userId}/library/`
          console.log('Loading library from:', libraryEndpoint)
          
          try {
            const libraryRes = await axios.get(libraryEndpoint, {
              headers: {
                Authorization: `Token ${token}`
              }
            })
            console.log('Library response:', libraryRes)
            library.value = libraryRes.data.library
            topGenres.value = libraryRes.data.top_genres
          } catch (error) {
            console.error('Library loading error:', error)
            library.value = []
            topGenres.value = []
          }

          // Load user's threads
          try {
            const threadsEndpoint = `http://127.0.0.1:8000/api/users/${userId}/threads/`
            console.log('Loading threads from:', threadsEndpoint)
            const threadsRes = await axios.get(threadsEndpoint, {
              headers: {
                Authorization: `Token ${token}`
              }
            })
            console.log('Threads response:', threadsRes.data)
            threads.value = threadsRes.data
          } catch (error) {
            console.error('Error loading threads:', error)
            threads.value = []
          }

          // Load user's top books
          try {
            const topBooksEndpoint = `http://127.0.0.1:8000/api/users/${userId}/top-books/`
            console.log('Loading top books from:', topBooksEndpoint)
            const topBooksResponse = await axios.get(topBooksEndpoint, {
              headers: { Authorization: `Token ${token}` }
            })
            console.log('Top books response:', topBooksResponse.data)
            topBooks.value = topBooksResponse.data
          } catch (error) {
            console.error('Error loading top books:', error)
            topBooks.value = []
          }
        } catch (error) {
          console.error('Error loading user data:', error)
        }
      }
    } else {
      console.error('No user data received')
      user.value = {}
      threads.value = []
      library.value = []
      topBooks.value = []
      topGenres.value = []
    }
  } catch (error) {
    console.error("프로필 로딩 실패:", error)
    if (error.response) {
      if (error.response.status === 401) {
        router.push('/login')
      } else {
        user.value = {}
        threads.value = []
        library.value = []
        topBooks.value = []
        topGenres.value = []
      }
    }
  }
}

const handleImageError = (e) => {
  console.log('Image load error, using default image')
  e.target.src = '/default-profile.png'
}

const toggleFollow = async () => {
  try {
    const token = localStorage.getItem('token')
    if (!token) {
      alert('로그인이 필요합니다.')
      return
    }

    const currentUserId = localStorage.getItem('userId')
    if (currentUserId === route.params.userId) {
      alert('자기 자신을 팔로우할 수 없습니다.')
      return
    }

    const newFollowStatus = !user.value.is_following
    user.value.is_following = newFollowStatus
    user.value.followers_count += newFollowStatus ? 1 : -1

    const response = await axios.post(
      `http://127.0.0.1:8000/accounts/api/follow/${route.params.userId}/`,
      {},
      {
        headers: {
          Authorization: `Token ${token}`
        }
      }
    )
    
    const profileRes = await axios.get(
      `http://127.0.0.1:8000/accounts/api/users/${route.params.userId}/profile/`,
      {
        headers: {
          Authorization: `Token ${token}`
        }
      }
    )
    
    user.value = profileRes.data
    user.value = { ...user.value }
  } catch (error) {
    console.error("팔로우 토글 실패:", error)
    user.value.is_following = !user.value.is_following
    user.value.followers_count += user.value.is_following ? 1 : -1
    user.value = { ...user.value }

    if (error.response) {
      if (error.response.status === 400) {
        alert(error.response.data.error || '팔로우할 수 없습니다.')
      } else if (error.response.status === 401) {
        alert('로그인이 필요합니다.')
      }
    }
  }
}

const goToThread = (threadId) => {
  router.push(`/threads/${threadId}`)
}

const goToBook = (bookId) => {
  router.push(`/books/${bookId}`)
}

const openLibraryEdit = () => {
  showLibraryEdit.value = true
}

const closeLibraryEdit = () => {
  showLibraryEdit.value = false
}

const updateLibrary = () => {
  loadProfileData()
}

onMounted(() => {
  loadProfileData()
})

watch(
  () => route.params.userId,
  (newUserId, oldUserId) => {
    if (newUserId !== oldUserId) {
      loadProfileData()
    }
  },
  { immediate: true }
)
</script>

<style scoped>
.profile-container {
  padding: 2rem;
  min-height: 100vh;
  background-color: #f5f5f5;
}

.content-wrapper {
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  gap: 2rem;
}

.left-sidebar {
  width: 300px;
  flex-shrink: 0;
}

.profile-box {
  background: white;
  padding: 2rem;
  border-radius: 1rem;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  text-align: center;
}

.profile-image {
  width: 150px;
  height: 150px;
  border-radius: 50%;
  margin-bottom: 1rem;
  object-fit: cover;
}

.profile-name {
  font-size: 1.5rem;
  font-weight: bold;
  margin-bottom: 0.5rem;
  color: #333;
}

.profile-username {
  color: #666;
  margin-bottom: 1rem;
}

.follow-stats {
  display: flex;
  justify-content: center;
  gap: 2rem;
  margin-bottom: 1.5rem;
}

.stat {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.stat-value {
  font-size: 1.2rem;
  font-weight: bold;
  color: #333;
}

.stat-label {
  font-size: 0.9rem;
  color: #666;
}

.follow-button {
  width: 100%;
  padding: 0.8rem;
  border: none;
  border-radius: 0.5rem;
  background-color: rgb(0, 105, 0);
  color: white;
  font-weight: bold;
  cursor: pointer;
  transition: background-color 0.2s;
}

.follow-button:hover {
  background-color: #0056b3;
}

.follow-button.following {
  background-color: #6c757d;
}

.follow-button.following:hover {
  background-color: #5a6268;
}

.right-box {
  flex: 1;
  background: white;
  border-radius: 1rem;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.tabs {
  display: flex;
  border-bottom: 1px solid #eee;
  padding: 0 1rem;
}

.tab-button {
  padding: 1rem 1.5rem;
  border: none;
  background: none;
  font-size: 1rem;
  color: #666;
  cursor: pointer;
  transition: all 0.2s;
  position: relative;
}

.tab-button:hover {
  color: #333;
}

.tab-button.active {
  color: rgb(0, 105, 0);
  font-weight: bold;
}

.tab-button.active::after {
  content: '';
  position: absolute;
  bottom: -1px;
  left: 0;
  right: 0;
  height: 2px;
  background-color: rgb(0, 105, 0);
}

.tab-content {
  padding: 2rem;
}

.empty-state {
  text-align: center;
  color: #666;
  padding: 2rem;
}

.library-grid {
  display: grid;
  grid-template-columns: repeat(5, minmax(0, 1fr));
  gap: 1.5rem;
  padding: 1rem;
  max-width: 1200px;
  margin: 0 auto;
}

@media (max-width: 1200px) {
  .library-grid {
    grid-template-columns: repeat(4, minmax(0, 1fr));
  }
}

@media (max-width: 992px) {
  .library-grid {
    grid-template-columns: repeat(3, minmax(0, 1fr));
  }
}

@media (max-width: 768px) {
  .library-grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
}

@media (max-width: 480px) {
  .library-grid {
    grid-template-columns: repeat(1, minmax(0, 1fr));
  }
}

.library-item {
  background: white;
  border-radius: 0.5rem;
  padding: 1rem;
  transition: transform 0.2s;
  cursor: pointer;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
}

.library-item:hover {
  transform: translateY(-2px);
}

.book-cover-container {
  width: 100%;
  display: flex;
  justify-content: center;
  margin-bottom: 0.5rem;
}

.book-cover {
  width: 100%;
  max-width: 180px;
  aspect-ratio: 2/3;
  object-fit: cover;
  border-radius: 0.5rem;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.book-title {
  font-size: 0.9rem;
  font-weight: bold;
  margin-bottom: 0.25rem;
  color: #333;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  line-height: 1.3;
  height: 2.6em;
  width: 100%;
}

.book-author {
  font-size: 0.8rem;
  color: #666;
  display: -webkit-box;
  -webkit-line-clamp: 1;
  -webkit-box-orient: vertical;
  overflow: hidden;
  width: 100%;
}

.threads-list {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.thread-item {
  background: white;
  border-radius: 1rem;
  padding: 1.5rem;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  transition: transform 0.2s;
  cursor: pointer;
}

.thread-item:hover {
  transform: translateY(-2px);
}

.thread-header {
  margin-bottom: 1rem;
}

.book-info {
  flex: 1; /* 텍스트 영역이 남는 공간 차지 */
  display: flex;
  gap: 1rem;
  align-items: center;
  overflow: hidden;
}

.book-cover {
  width: 80px;
  height: 120px;
  object-fit: cover;
  border-radius: 0.5rem;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.book-details {
  flex: 1;
}

.book-title {
  font-size: 1.1rem;
  font-weight: bold;
  color: #333;
  margin-bottom: 0.5rem;
}

.thread-meta {
  display: flex;
  gap: 1rem;
  color: #666;
  font-size: 0.9rem;
}

.author {
  font-weight: 500;
}

.date {
  color: #888;
}

.thread-body {
  margin-bottom: 1rem;
}

.thread-title {
  font-size: 1.3rem;
  font-weight: bold;
  color: #333;
  margin-bottom: 0.5rem;
}

.thread-content {
  color: #666;
  line-height: 1.6;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.thread-footer {
  display: flex;
  justify-content: space-between;
  padding-top: 1rem;
  border-top: 1px solid #eee;
}

.engagement-stats {
  display: flex;
  gap: 1.5rem;
  color: #666;
  font-size: 0.9rem;
}

.thread-meta {
  display: flex;
  gap: 15px;
  color: #888;
}

.interactions {
  display: flex;
  gap: 15px;
  color: #888;
}

.library-actions {
  display: flex;
  justify-content: flex-end;
  margin-bottom: 1rem;
  padding: 0 1rem;
}

.edit-btn {
  background: rgb(0, 105, 0);
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 0.5rem;
  font-weight: bold;
  cursor: pointer;
  transition: background-color 0.2s;
}

.edit-btn:hover {
  background: rgb(0, 85, 0);
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-content {
  width: 90%;
  max-width: 1200px;
  max-height: 90vh;
  overflow-y: auto;
}

.top-books-section {
  margin-bottom: 10px;
  padding: 1.5rem;
  background: white;
  border-radius: 1rem;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.section-title {
  font-size: 1.2rem;
  font-weight: bold;
  margin-bottom: 1rem;
  color: #333;
  margin-top: 10px;
}

.top-books-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1.5rem;
}

.top-book-item {
  position: relative;
  background: white;
  border-radius: 0.5rem;
  padding: 1rem;
  transition: transform 0.2s;
  cursor: pointer;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
}

.top-book-item:hover {
  transform: translateY(-2px);
}

.rank-badge {
  position: absolute;
  top: 0.5rem;
  left: 0.5rem;
  background: rgb(0, 105, 0);
  color: white;
  padding: 0.25rem 0.5rem;
  border-radius: 0.25rem;
  font-size: 0.8rem;
  font-weight: bold;
}

.top-book-item .book-cover-container {
  width: 100%;
  display: flex;
  justify-content: center;
  margin-bottom: 0.5rem;
}

.top-book-item .book-cover {
  width: 100%;
  max-width: 180px;
  aspect-ratio: 2/3;
  object-fit: cover;
  border-radius: 0.5rem;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.top-book-item .book-title {
  font-size: 0.9rem;
  font-weight: bold;
  margin-bottom: 0.25rem;
  color: #333;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  line-height: 1.3;
  height: 2.6em;
  width: 100%;
}

.top-book-item .book-author {
  font-size: 0.8rem;
  color: #666;
  display: -webkit-box;
  -webkit-line-clamp: 1;
  -webkit-box-orient: vertical;
  overflow: hidden;
  width: 100%;
}

.top-genres-section {
  margin-bottom: 2rem;
  padding: 1.5rem;
  background: white;
  border-radius: 1rem;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.top-genres-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1.5rem;
}

.genre-item {
  position: relative;
  background: #f8f9fa;
  border-radius: 0.5rem;
  padding: 1.5rem;
  text-align: center;
  transition: transform 0.2s;
}

.genre-item:hover {
  transform: translateY(-2px);
}

.genre-name {
  font-size: 1.1rem;
  font-weight: bold;
  color: #333;
  margin-bottom: 0.5rem;
}

.genre-count {
  font-size: 0.9rem;
  color: #666;
}
</style>
