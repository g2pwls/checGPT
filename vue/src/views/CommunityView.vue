<template>
  <div class="community-view">
    <div class="community-header">
      <h1>{{ book.title }} Thread</h1>
      <button @click="isWriteModalOpen = true" class="write-btn">글쓰기</button>
    </div>

    <!-- 카테고리 탭 -->
    <div class="category-tabs">
      <button 
        @click="selectedCategory = ''"
        :class="{ active: selectedCategory === '' }"
        class="tab-btn"
      >
        전체
      </button>
      <button 
        v-for="category in categories" 
        :key="category.value"
        @click="selectedCategory = category.value"
        :class="{ active: selectedCategory === category.value }"
        class="tab-btn"
      >
        {{ category.label }}
      </button>
    </div>

    <!-- 인기글 섹션 -->
    <div v-if="popularPosts.length > 0" class="popular-posts">
      <h2>🔥 인기글</h2>
      <div class="posts-grid">
        <div v-for="post in popularPosts" :key="post.id" class="post-card popular">
          <div class="post-content-row">
            <div class="post-left">
              <span class="category-tag">{{ post.category_display }}</span>
              <span class="post-title">{{ post.title }}</span>
            </div>
            <div class="post-right">
              <span class="writer">{{ post.writer.username }}</span>
              <span class="date">{{ formatSimpleDate(post.created_at) }}</span>
              <button @click="toggleLike(post)" class="like-btn" :class="{ 'liked': post.is_liked }">
                {{ post.is_liked ? '❤️' : '🤍' }} {{ post.likes_count }}
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 일반 게시글 목록 -->
    <div class="posts-container">
      <div v-if="filteredPosts.length === 0" class="no-posts">
        작성된 게시글이 없습니다.
      </div>
      <div v-else v-for="post in filteredPosts" :key="post.id" class="post-card">
        <div class="post-content-row">
          <div class="post-left">
            <span class="category-tag">{{ post.category_display }}</span>
            <router-link 
              :to="{ name: 'communityDetail', params: { postId: post.id }}" 
              class="post-title"
            >
              {{ post.title }}
            </router-link>
          </div>
          <div class="post-right">
            <span class="writer">{{ post.writer.username }}</span>
            <span class="date">{{ formatSimpleDate(post.created_at) }}</span>
            <button @click="toggleLike(post)" class="like-btn" :class="{ 'liked': post.is_liked }">
              {{ post.is_liked ? '❤️' : '🤍' }} {{ post.likes_count }}
            </button>
            <div v-if="isMyPost(post)" class="action-buttons">
              <button @click="editPost(post)" class="edit-btn">수정</button>
              <button @click="deletePost(post.id)" class="delete-btn">삭제</button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 글쓰기/수정 모달 -->
    <div v-if="isWriteModalOpen" class="modal">
      <div class="modal-content">
        <h2>{{ editingPost ? '게시글 수정' : '새 게시글 작성' }}</h2>
        <select v-model="postForm.category" class="select-field">
          <option value="">말머리를 선택하세요</option>
          <option v-for="category in categories" :key="category.value" :value="category.value">
            {{ category.label }}
          </option>
        </select>
        <input 
          v-model="postForm.title" 
          type="text" 
          placeholder="제목을 입력하세요"
          class="input-field"
        >
        <textarea 
          v-model="postForm.content" 
          placeholder="내용을 입력하세요"
          class="textarea-field"
        ></textarea>
        <div class="modal-actions">
          <button @click="submitPost" class="submit-btn">
            {{ editingPost ? '수정하기' : '작성하기' }}
          </button>
          <button @click="closeModal" class="cancel-btn">취소</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      book: {},
      posts: [],
      selectedCategory: '',
      isWriteModalOpen: false,
      postForm: {
        category: '',
        title: '',
        content: ''
      },
      editingPost: null,
      categories: [
        { value: 'chat', label: '잡담' },
        { value: 'share', label: '나눔' },
        { value: 'reading', label: '읽는 중' },
        { value: 'finished', label: '읽은 후' }
      ],
      commentForms: {},
    }
  },
  computed: {
    popularPosts() {
      return this.posts.filter(post => post.is_popular);
    },
    filteredPosts() {
      if (!this.selectedCategory) return this.posts;
      return this.posts.filter(post => post.category === this.selectedCategory);
    }
  },
  async created() {
    await this.loadBookData();
    await this.loadPosts();
  },
  methods: {
    async loadBookData() {
      try {
        const token = localStorage.getItem('token');
        const response = await axios.get(
          `http://127.0.0.1:8000/api/books/${this.$route.params.bookId}/`,
          {
            headers: { Authorization: `Token ${token}` }
          }
        );
        this.book = response.data;
      } catch (error) {
        console.error('책 정보 로딩 실패:', error);
      }
    },
    async loadPosts() {
      try {
        const token = localStorage.getItem('token');
        const response = await axios.get(
          `http://127.0.0.1:8000/api/books/${this.$route.params.bookId}/community/`,
          {
            headers: { Authorization: `Token ${token}` }
          }
        );
        this.posts = response.data;
      } catch (error) {
        console.error('게시글 로딩 실패:', error);
      }
    },
    formatDate(dateString) {
      return new Date(dateString).toLocaleDateString('ko-KR', {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      });
    },
    formatSimpleDate(dateString) {
      const date = new Date(dateString);
      const year = date.getFullYear().toString().slice(2);
      const month = String(date.getMonth() + 1).padStart(2, '0');
      const day = String(date.getDate()).padStart(2, '0');
      return `${year}/${month}/${day}`;
    },
    isMyPost(post) {
      const userId = localStorage.getItem('userId');
      return post.writer.id === parseInt(userId);
    },
    async submitPost() {
      if (!this.postForm.category) {
        alert('말머리를 선택해주세요.');
        return;
      }

      try {
        const token = localStorage.getItem('token');
        const data = {
          category: this.postForm.category,
          title: this.postForm.title,
          content: this.postForm.content,
          book_id: this.book.id
        };

        if (this.editingPost) {
          await axios.put(
            `http://127.0.0.1:8000/api/community/${this.editingPost.id}/`,
            data,
            {
              headers: { Authorization: `Token ${token}` }
            }
          );
        } else {
          await axios.post(
            `http://127.0.0.1:8000/api/books/${this.book.id}/community/`,
            data,
            {
              headers: { Authorization: `Token ${token}` }
            }
          );
        }

        await this.loadPosts();
        this.closeModal();
      } catch (error) {
        console.error('게시글 저장 실패:', error);
        if (error.response?.data?.detail) {
          alert(error.response.data.detail);
        } else {
          alert('게시글 저장에 실패했습니다.');
        }
      }
    },
    editPost(post) {
      this.editingPost = post;
      this.postForm = {
        category: post.category,
        title: post.title,
        content: post.content
      };
      this.isWriteModalOpen = true;
    },
    async deletePost(postId) {
      if (!confirm('정말 삭제하시겠습니까?')) return;

      try {
        const token = localStorage.getItem('token');
        await axios.delete(
          `http://127.0.0.1:8000/api/community/${postId}/`,
          {
            headers: { Authorization: `Token ${token}` }
          }
        );
        await this.loadPosts();
      } catch (error) {
        console.error('게시글 삭제 실패:', error);
        alert('게시글 삭제에 실패했습니다.');
      }
    },
    closeModal() {
      this.isWriteModalOpen = false;
      this.editingPost = null;
      this.postForm = {
        category: '',
        title: '',
        content: ''
      };
    },
    async toggleLike(post) {
      try {
        const token = localStorage.getItem('token');
        if (!token) {
          alert('로그인이 필요합니다.');
          return;
        }

        const response = await axios.post(
          `http://127.0.0.1:8000/api/community/${post.id}/like/`,
          {},
          {
            headers: { Authorization: `Token ${token}` }
          }
        );

        // 게시글 상태 업데이트
        post.is_liked = response.data.liked;
        post.likes_count = response.data.likes_count;
        post.is_popular = response.data.is_popular;

        // 인기글 상태가 변경되었다면 게시글 목록 새로고침
        if (post.is_popular !== response.data.is_popular) {
          await this.loadPosts();
        }
      } catch (error) {
        console.error('좋아요 토글 실패:', error);
        alert('좋아요 처리에 실패했습니다.');
      }
    },
    isMyComment(comment) {
      const userId = localStorage.getItem('userId');
      return comment.writer.id === parseInt(userId);
    },
    async submitComment(postId) {
      if (!this.commentForms[postId]?.trim()) {
        return;
      }

      try {
        const token = localStorage.getItem('token');
        await axios.post(
          `http://127.0.0.1:8000/api/community/${postId}/comments/`,
          { content: this.commentForms[postId] },
          {
            headers: { Authorization: `Token ${token}` }
          }
        );
        
        this.commentForms[postId] = '';
        await this.loadPosts();
      } catch (error) {
        console.error('댓글 작성 실패:', error);
        alert('댓글 작성에 실패했습니다.');
      }
    },
    async deleteComment(commentId, postId) {
      if (!confirm('댓글을 삭제하시겠습니까?')) return;

      try {
        const token = localStorage.getItem('token');
        await axios.delete(
          `http://127.0.0.1:8000/api/community/comments/${commentId}/`,
          {
            headers: { Authorization: `Token ${token}` }
          }
        );
        await this.loadPosts();
      } catch (error) {
        console.error('댓글 삭제 실패:', error);
        alert('댓글 삭제에 실패했습니다.');
      }
    }
  }
}
</script>

<style scoped>
.community-view {
  max-width: 800px;
  margin: 40px auto;
  padding: 0 20px;
}

.community-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
}

.category-tabs {
  display: flex;
  gap: 10px;
  margin-bottom: 20px;
}

.tab-btn {
  padding: 8px 16px;
  border: none;
  border-radius: 20px;
  background: #f5f5f5;
  color: #666;
  cursor: pointer;
  transition: all 0.3s ease;
}

.tab-btn.active {
  background: #4CAF50;
  color: white;
}

.popular-posts {
  margin-bottom: 30px;
}

.popular-posts h2 {
  margin-bottom: 15px;
  color: #e74c3c;
}

.post-card {
  background: white;
  border-radius: 8px;
  padding: 10px 20px 10px 20px;
  margin-bottom: 20px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.post-card.popular {
  border: 2px solid #e74c3c;
}

.post-content-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%;
  padding: 10px;
}

.post-left {
  display: flex;
  align-items: center;
  gap: 12px;
  flex: 1;
}

.post-right {
  display: flex;
  align-items: center;
  gap: 16px;
}

.category-tag {
  background: #f0f0f0;
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 0.8rem;
  color: #666;
  min-width: 60px;
  text-align: center;
}

.post-title {
  text-decoration: none;
  color: #333;
  font-weight: 500;
  transition: color 0.2s ease;
}

.post-title:hover {
  color: #4CAF50;
}

.writer {
  color: #666;
  font-size: 0.9rem;
}

.date {
  color: #888;
  font-size: 0.9rem;
}

.action-buttons {
  display: flex;
  gap: 8px;
  margin-left: 8px;
}

.edit-btn,
.delete-btn {
  padding: 4px 8px;
  font-size: 0.8rem;
  border-radius: 4px;
}

.post-card {
  transition: all 0.2s ease;
}

.post-card:hover {
  background-color: #f8f9fa;
}

.like-btn {
  display: flex;
  align-items: center;
  gap: 4px;
  padding: 4px 8px;
  border: none;
  background: none;
  cursor: pointer;
  transition: all 0.2s ease;
}

.like-btn:hover {
  background: rgba(0, 0, 0, 0.05);
  border-radius: 4px;
}

.like-btn.liked {
  color: #e74c3c;
}

.write-btn {
  padding: 10px 20px;
  background: #4CAF50;
  color: white;
  border: none;
  border-radius: 20px;
  cursor: pointer;
  font-weight: bold;
  transition: all 0.3s ease;
}

.write-btn:hover {
  background: #45a049;
}

.modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0,0,0,0.5);
  display: flex;
  justify-content: center;
  align-items: center;
}

.modal-content {
  background: white;
  padding: 30px;
  border-radius: 8px;
  width: 90%;
  max-width: 600px;
}

.select-field,
.input-field,
.textarea-field {
  width: 100%;
  padding: 10px;
  margin-bottom: 15px;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.textarea-field {
  height: 200px;
  resize: vertical;
}

.modal-actions {
  display: flex;
  gap: 10px;
  justify-content: flex-end;
}

.submit-btn,
.cancel-btn {
  padding: 8px 20px;
  border: none;
  border-radius: 20px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.submit-btn {
  background: #4CAF50;
  color: white;
}

.cancel-btn {
  background: #9e9e9e;
  color: white;
}

.no-posts {
  text-align: center;
  padding: 40px;
  color: #666;
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.comments-section,
.post-content,
.comments-container,
.comments-list,
.comment,
.comment-header,
.comment-writer,
.comment-date,
.comment-content,
.delete-comment-btn,
.comment-form,
.submit-comment-btn {
  display: none;
}
</style> 