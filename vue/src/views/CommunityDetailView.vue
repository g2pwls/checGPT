<template>
  <div class="community-detail-view">
    <!-- 게시글 상세 내용 -->
    <div v-if="post" class="post-detail">
      <div class="post-header">
        <h2>{{ post.title }}</h2>
        <div class="post-meta">
          <span class="category-tag">{{ post.category_display }}</span>
          <span class="writer">작성자: {{ post.writer.username }}</span>
          <span class="date">{{ formatDate(post.created_at) }}</span>
        </div>
      </div>

      <div class="post-content">
        {{ post.content }}
      </div>

      <div class="post-actions">
        <button @click="toggleLike" class="like-btn" :class="{ 'liked': post.is_liked }">
          {{ post.is_liked ? '❤️' : '🤍' }} {{ post.likes_count }}
        </button>
        <div v-if="isMyPost" class="action-buttons">
          <button @click="editPost" class="edit-btn">수정</button>
          <button @click="deletePost" class="delete-btn">삭제</button>
        </div>
      </div>

      <!-- 댓글 섹션 -->
      <div class="comments-section">
        <h3>댓글</h3>
        <div class="comments-list">
          <div v-if="post.comments.length === 0" class="no-comments">
            아직 작성된 댓글이 없습니다.
          </div>
          <div v-else v-for="comment in post.comments" :key="comment.id" class="comment">
            <div class="comment-header">
              <span class="comment-writer">{{ comment.writer.username }}</span>
              <span class="comment-date">{{ formatDate(comment.created_at) }}</span>
            </div>
            <div class="comment-content">{{ comment.content }}</div>
            <button 
              v-if="isMyComment(comment)" 
              @click="deleteComment(comment.id)" 
              class="delete-comment-btn"
            >
              삭제
            </button>
          </div>
        </div>

        <!-- 댓글 작성 폼 -->
        <div class="comment-form">
          <input 
            v-model="commentContent" 
            type="text" 
            placeholder="댓글을 입력하세요"
            @keyup.enter="submitComment"
          >
          <button @click="submitComment" class="submit-comment-btn">
            댓글 작성
          </button>
        </div>
      </div>
    </div>

    <!-- 수정 모달 -->
    <div v-if="isEditModalOpen" class="modal">
      <div class="modal-content">
        <h2>게시글 수정</h2>
        <select v-model="editForm.category" class="select-field">
          <option value="">말머리를 선택하세요</option>
          <option v-for="category in categories" :key="category.value" :value="category.value">
            {{ category.label }}
          </option>
        </select>
        <input 
          v-model="editForm.title" 
          type="text" 
          placeholder="제목을 입력하세요"
          class="input-field"
        >
        <textarea 
          v-model="editForm.content" 
          placeholder="내용을 입력하세요"
          class="textarea-field"
        ></textarea>
        <div class="modal-actions">
          <button @click="updatePost" class="submit-btn">수정하기</button>
          <button @click="closeEditModal" class="cancel-btn">취소</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import { useRouter } from 'vue-router';

export default {
  data() {
    return {
      post: null,
      commentContent: '',
      isEditModalOpen: false,
      editForm: {
        category: '',
        title: '',
        content: ''
      },
      categories: [
        { value: 'chat', label: '잡담' },
        { value: 'share', label: '나눔' },
        { value: 'reading', label: '읽는 중' },
        { value: 'finished', label: '읽은 후' }
      ]
    }
  },
  computed: {
    isMyPost() {
      const userId = localStorage.getItem('userId');
      return this.post?.writer.id === parseInt(userId);
    }
  },
  async created() {
    await this.loadPost();
  },
  methods: {
    async loadPost() {
      try {
        const token = localStorage.getItem('token');
        const response = await axios.get(
          `http://127.0.0.1:8000/api/community/${this.$route.params.postId}/`,
          {
            headers: { Authorization: `Token ${token}` }
          }
        );
        this.post = response.data;
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
    isMyComment(comment) {
      const userId = localStorage.getItem('userId');
      return comment.writer.id === parseInt(userId);
    },
    async submitComment() {
      if (!this.commentContent.trim()) return;

      try {
        const token = localStorage.getItem('token');
        await axios.post(
          `http://127.0.0.1:8000/api/community/${this.post.id}/comments/`,
          { 
            content: this.commentContent,
            post: this.post.id  // post ID를 추가
          },
          {
            headers: { Authorization: `Token ${token}` }
          }
        );
        
        this.commentContent = '';
        await this.loadPost();
      } catch (error) {
        console.error('댓글 작성 실패:', error);
        alert('댓글 작성에 실패했습니다.');
      }
    },
    async deleteComment(commentId) {
      if (!confirm('댓글을 삭제하시겠습니까?')) return;

      try {
        const token = localStorage.getItem('token');
        await axios.delete(
          `http://127.0.0.1:8000/api/community/comments/${commentId}/`,
          {
            headers: { Authorization: `Token ${token}` }
          }
        );
        await this.loadPost();
      } catch (error) {
        console.error('댓글 삭제 실패:', error);
        alert('댓글 삭제에 실패했습니다.');
      }
    },
    async toggleLike() {
      try {
        const token = localStorage.getItem('token');
        const response = await axios.post(
          `http://127.0.0.1:8000/api/community/${this.post.id}/like/`,
          {},
          {
            headers: { Authorization: `Token ${token}` }
          }
        );
        
        this.post.is_liked = response.data.liked;
        this.post.likes_count = response.data.likes_count;
        this.post.is_popular = response.data.is_popular;
      } catch (error) {
        console.error('좋아요 토글 실패:', error);
        alert('좋아요 처리에 실패했습니다.');
      }
    },
    editPost() {
      this.editForm = {
        category: this.post.category,
        title: this.post.title,
        content: this.post.content
      };
      this.isEditModalOpen = true;
    },
    async updatePost() {
      try {
        const token = localStorage.getItem('token');
        await axios.put(
          `http://127.0.0.1:8000/api/community/${this.post.id}/`,
          this.editForm,
          {
            headers: { Authorization: `Token ${token}` }
          }
        );
        
        await this.loadPost();
        this.closeEditModal();
      } catch (error) {
        console.error('게시글 수정 실패:', error);
        alert('게시글 수정에 실패했습니다.');
      }
    },
    async deletePost() {
      if (!confirm('정말 삭제하시겠습니까?')) return;

      try {
        const token = localStorage.getItem('token');
        await axios.delete(
          `http://127.0.0.1:8000/api/community/${this.post.id}/`,
          {
            headers: { Authorization: `Token ${token}` }
          }
        );
        
        const router = useRouter();
        router.push({ name: 'community', params: { bookId: this.post.book.id }});
      } catch (error) {
        console.error('게시글 삭제 실패:', error);
        alert('게시글 삭제에 실패했습니다.');
      }
    },
    closeEditModal() {
      this.isEditModalOpen = false;
      this.editForm = {
        category: '',
        title: '',
        content: ''
      };
    }
  }
}
</script>

<style scoped>
.community-detail-view {
  max-width: 800px;
  margin: 40px auto;
  padding: 0 20px;
}

.post-detail {
  background: white;
  border-radius: 8px;
  padding: 30px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.post-header {
  margin-bottom: 20px;
}

.post-header h2 {
  margin-bottom: 10px;
  color: #333;
}

.post-meta {
  display: flex;
  gap: 15px;
  color: #666;
  font-size: 0.9rem;
}

.category-tag {
  background: #f0f0f0;
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 0.8rem;
  color: #666;
}

.post-content {
  margin: 20px 0;
  line-height: 1.6;
  color: #333;
}

.post-actions {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 20px;
  padding-top: 20px;
  border-top: 1px solid #eee;
}

.like-btn {
  display: flex;
  align-items: center;
  gap: 4px;
  padding: 8px 16px;
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

.action-buttons {
  display: flex;
  gap: 10px;
}

.edit-btn,
.delete-btn {
  padding: 6px 12px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.9rem;
}

.edit-btn {
  background: #4CAF50;
  color: white;
}

.delete-btn {
  background: #f44336;
  color: white;
}

.comments-section {
  margin-top: 30px;
  padding-top: 20px;
  border-top: 1px solid #eee;
}

.comments-section h3 {
  margin-bottom: 20px;
  color: #333;
}

.no-comments {
  text-align: center;
  padding: 20px;
  color: #666;
  background: #f8f9fa;
  border-radius: 4px;
}

.comment {
  padding: 15px;
  background: #f8f9fa;
  border-radius: 4px;
  margin-bottom: 10px;
  position: relative;
}

.comment-header {
  display: flex;
  gap: 10px;
  margin-bottom: 5px;
}

.comment-writer {
  font-weight: 500;
  color: #333;
}

.comment-date {
  color: #888;
  font-size: 0.8rem;
}

.comment-content {
  color: #555;
}

.delete-comment-btn {
  position: absolute;
  right: 10px;
  top: 10px;
  padding: 2px 6px;
  font-size: 0.8rem;
  color: #dc3545;
  background: none;
  border: none;
  cursor: pointer;
}

.delete-comment-btn:hover {
  text-decoration: underline;
}

.comment-form {
  margin-top: 20px;
  display: flex;
  gap: 10px;
}

.comment-form input {
  flex: 1;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.submit-comment-btn {
  padding: 10px 20px;
  background: #4CAF50;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.submit-comment-btn:hover {
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
  border-radius: 4px;
  cursor: pointer;
}

.submit-btn {
  background: #4CAF50;
  color: white;
}

.cancel-btn {
  background: #9e9e9e;
  color: white;
}
</style> 