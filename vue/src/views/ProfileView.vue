<template>
  <div class="profile-container">
    <section class="profile-section">
      <img
        :src="getProfileImageUrl(user.profile_image)"
        alt="프로필 사진"
        class="profile-image"
        @error="handleImageError"
      />
      <h2>{{ user.name }}</h2>
      <p class="username">@{{ user.username }}</p>
      
      <!-- Follower/Following counts -->
      <div class="follow-stats">
        <div class="stat-item">
          <span class="stat-value">{{ user.followers_count || 0 }}</span>
          <span class="stat-label">팔로워</span>
        </div>
        <div class="stat-item">
          <span class="stat-value">{{ user.following_count || 0 }}</span>
          <span class="stat-label">팔로잉</span>
        </div>
      </div>

      <div class="interests" v-if="user.interests">
        <span v-for="interest in user.interests" :key="interest" class="interest-tag">
          {{ interest }}
        </span>
      </div>
      
      <!-- Follow button only shows on other users' profiles -->
      <button v-if="!isOwnProfile" @click="toggleFollow" class="follow-btn" :class="{ 'following': isFollowing }">
        {{ isFollowing ? '팔로잉' : '+ 팔로우' }}
      </button>
    </section>

    <!-- Tabs -->
    <div class="tabs">
      <button 
        @click="activeTab = 'library'" 
        :class="{ active: activeTab === 'library' }"
        class="tab-btn"
      >
        {{ user.name }}님의 서재
      </button>
      <button 
        @click="activeTab = 'threads'" 
        :class="{ active: activeTab === 'threads' }"
        class="tab-btn"
      >
        {{ user.name }}님의 스레드
      </button>
    </div>

    <!-- Threads Tab -->
    <section v-if="activeTab === 'threads'" class="threads-section">
      <div v-if="threads.length === 0" class="no-threads">
        작성한 스레드가 없습니다.
      </div>
      <div v-else class="threads-list">
        <div v-for="thread in threads" :key="thread.id" class="thread-item" @click="goToThread(thread.id)">
          <h4>{{ thread.title }}</h4>
          <p class="thread-meta">
            ❤️ {{ thread.likes_count }} ・ 💬 {{ thread.comments_count }}
          </p>
          <p class="thread-book">📚 {{ thread.book.title }}</p>
        </div>
      </div>
    </section>

    <!-- Library Tab -->
    <section v-if="activeTab === 'library'" class="library-section">
      <div v-if="library.length === 0" class="no-books">
        서재에 추가된 책이 없습니다.
      </div>
      <div v-else class="library-grid">
        <div v-for="item in library" :key="item.id" class="book-item" @click="goToBook(item.book.id)">
          <img :src="item.book.cover" :alt="item.book.title" class="book-cover" />
          <h4>{{ item.book.title }}</h4>
          <p class="book-author">{{ item.book.author }}</p>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref, onMounted, computed, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import axios from 'axios'

const route = useRoute()
const router = useRouter()
const user = ref({})
const threads = ref([])
const library = ref([])
const isFollowing = ref(false)
const activeTab = ref('library')

// Check if this is the user's own profile
const isOwnProfile = computed(() => {
  const currentUserId = localStorage.getItem('userId')
  return !route.params.userId || route.params.userId === currentUserId
})

const getProfileImageUrl = (imagePath) => {
  if (!imagePath) return '/default-profile.png'
  // If the image path is already a full URL, return it as is
  if (imagePath.startsWith('http')) return imagePath
  // Otherwise, prepend the Django media URL
  return `http://127.0.0.1:8000${imagePath}`
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
    
    // Always use the user-specific endpoint
    const endpoint = `http://127.0.0.1:8000/accounts/api/users/${userId}/profile/`
    
    console.log('Loading profile from:', endpoint)
    const res = await axios.get(endpoint, {
      headers: {
        Authorization: `Token ${token}`
      }
    })
    console.log('Profile response:', res.data)
    
    // Ensure we have a valid user object
    if (res.data) {
      user.value = res.data
      console.log('User value after setting:', user.value)
      isFollowing.value = user.value.is_following

      // Load threads and library
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
            library.value = libraryRes.data
          } catch (error) {
            console.error('Library loading error:', error)
            if (error.response) {
              console.error('Error response:', error.response.data)
              console.error('Error status:', error.response.status)
            }
            library.value = [] // Reset library on error
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
            if (error.response) {
              console.error('Error response:', error.response.data)
              console.error('Error status:', error.response.status)
              if (error.response.status === 404) {
                threads.value = [] // User not found
              } else if (error.response.status === 500) {
                console.error('Server error loading threads:', error.response.data)
                threads.value = [] // Server error
              }
            }
            threads.value = [] // Reset threads on error
          }
        } catch (error) {
          console.error('Error loading user data:', error)
          if (error.response) {
            console.error('Error response:', error.response.data)
          }
        }
      } else {
        console.error('No user ID available')
      }
    } else {
      console.error('No user data received')
      user.value = {}
      threads.value = []
      library.value = []
    }
  } catch (error) {
    console.error("프로필 로딩 실패:", error)
    if (error.response) {
      console.error("Error response:", error.response.data)
      if (error.response.status === 401) {
        router.push('/login')
      } else if (error.response.status === 404) {
        // Handle user not found
        user.value = {}
        threads.value = []
        library.value = []
      } else if (error.response.status === 500) {
        console.error('Server error loading profile:', error.response.data)
        // Handle server error
        user.value = {}
        threads.value = []
        library.value = []
      }
    }
  }
}

// Watch for route changes to reload profile data
watch(
  () => route.params.userId,
  (newUserId, oldUserId) => {
    if (newUserId !== oldUserId) {
      loadProfileData()
    }
  },
  { immediate: true }
)

const handleImageError = (e) => {
  console.log('Image load error, using default image')
  e.target.src = '/default-profile.png'
}

onMounted(() => {
  loadProfileData()
})

const editProfile = () => {
  router.push('/profile/edit')
}

const toggleFollow = async () => {
  try {
    const token = localStorage.getItem('token')
    if (!token) {
      alert('로그인이 필요합니다.')
      return
    }

    // Check if trying to follow self
    const currentUserId = localStorage.getItem('userId')
    if (currentUserId === route.params.userId) {
      alert('자기 자신을 팔로우할 수 없습니다.')
      return
    }

    // Optimistically update UI
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
    
    // Refresh profile data to get updated counts
    const profileRes = await axios.get(
      `http://127.0.0.1:8000/accounts/api/users/${route.params.userId}/profile/`,
      {
        headers: {
          Authorization: `Token ${token}`
        }
      }
    )
    
    // Update with fresh data from server
    user.value = profileRes.data
    
    // Force Vue to recognize the changes
    user.value = { ...user.value }
  } catch (error) {
    console.error("팔로우 토글 실패:", error)
    // Revert optimistic update on error
    user.value.is_following = !user.value.is_following
    user.value.followers_count += user.value.is_following ? 1 : -1
    user.value = { ...user.value }

    if (error.response) {
      console.error("Error response:", error.response.data)
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
</script>

<style scoped>
.profile-container {
  max-width: 800px;
  margin: 40px auto;
  padding: 20px;
}

.profile-section {
  text-align: center;
  margin-bottom: 40px;
}

.profile-image {
  width: 150px;
  height: 150px;
  border-radius: 50%;
  object-fit: cover;
  margin-bottom: 20px;
}

.username {
  color: #666;
  margin-bottom: 15px;
}

.follow-stats {
  display: flex;
  justify-content: center;
  gap: 30px;
  margin: 20px 0;
}

.stat-item {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.stat-value {
  font-size: 18px;
  font-weight: bold;
  color: #333;
}

.stat-label {
  font-size: 14px;
  color: #666;
}

.interests {
  margin: 20px 0;
}

.interest-tag {
  display: inline-block;
  background: #f0f0f0;
  padding: 5px 12px;
  border-radius: 15px;
  margin: 0 5px 5px 0;
  font-size: 14px;
}

.follow-btn {
  padding: 8px 20px;
  border-radius: 20px;
  border: none;
  cursor: pointer;
  font-weight: bold;
  transition: all 0.3s ease;
  background-color: #f0f0f0;
  color: #333;
}

.follow-btn.following {
  background-color: #ddd;
}

/* Tabs */
.tabs {
  display: flex;
  justify-content: center;
  gap: 20px;
  margin-bottom: 30px;
}

.tab-btn {
  padding: 10px 20px;
  border: none;
  background: none;
  font-size: 16px;
  cursor: pointer;
  border-bottom: 2px solid transparent;
  transition: all 0.3s ease;
}

.tab-btn.active {
  border-bottom-color: #e74c3c;
  color: #e74c3c;
}

/* Threads Section */
.threads-section {
  margin-top: 20px;
}

.thread-item {
  background: white;
  padding: 15px;
  border-radius: 8px;
  margin-bottom: 10px;
  cursor: pointer;
  transition: transform 0.2s ease;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.thread-item:hover {
  transform: translateY(-2px);
}

.thread-meta {
  color: #666;
  font-size: 14px;
  margin-top: 5px;
}

.thread-book {
  color: #666;
  font-size: 14px;
  margin-top: 5px;
}

/* Library Section */
.library-section {
  margin-top: 20px;
}

.library-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
  gap: 20px;
  padding: 20px 0;
}

.book-item {
  background: white;
  padding: 10px;
  border-radius: 8px;
  cursor: pointer;
  transition: transform 0.2s ease;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.book-item:hover {
  transform: translateY(-2px);
}

.book-cover {
  width: 100%;
  height: 200px;
  object-fit: cover;
  border-radius: 4px;
  margin-bottom: 10px;
}

.book-author {
  color: #666;
  font-size: 14px;
  margin-top: 5px;
}

.no-threads, .no-books {
  text-align: center;
  color: #666;
  padding: 40px;
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}
</style>
