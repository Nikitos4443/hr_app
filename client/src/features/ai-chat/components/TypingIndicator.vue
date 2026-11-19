<template>
  <div class="typing" role="status" aria-label="The assistant is typing">
    <span class="typing__dot" />
    <span class="typing__dot" />
    <span class="typing__dot" />
  </div>
</template>

<style scoped>
.typing {
  display: inline-flex;
  gap: 4px;
  padding: 14px 16px;
  border-radius: 16px 16px 16px 4px;
  background: var(--p-content-hover-background);
}

.typing__dot {
  width: 7px;
  height: 7px;
  border-radius: 50%;
  background: var(--p-text-muted-color);
  animation: typing-bounce 1.2s infinite ease-in-out;
}

.typing__dot:nth-child(2) {
  animation-delay: 0.15s;
}

.typing__dot:nth-child(3) {
  animation-delay: 0.3s;
}

@keyframes typing-bounce {
  0%,
  60%,
  100% {
    opacity: 0.4;
    transform: translateY(0);
  }
  30% {
    opacity: 1;
    transform: translateY(-4px);
  }
}

@media (prefers-reduced-motion: reduce) {
  .typing__dot {
    animation: none;
  }
}
</style>
