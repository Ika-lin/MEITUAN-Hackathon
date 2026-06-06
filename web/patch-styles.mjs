import { readFileSync, writeFileSync } from 'fs'

const file = 'f:\\文档\\GitHub\\MEITUAN-Hackathon-main\\web\\src\\style.css'
const c = readFileSync(file, 'utf8')

const customizeStyles = `

/* ========== Customize Page (方案选择) ========== */

.customize-page {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 50;
}

.customize-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(10, 10, 10, 0.63);
  backdrop-filter: blur(2px);
}

.customize-container {
  position: relative;
  z-index: 51;
  width: 90%;
  max-width: 340px;
  background: linear-gradient(135deg, rgba(255, 107, 107, 0.95) 0%, rgba(255, 159, 64, 0.95) 50%, rgba(255, 227, 102, 0.95) 100%);
  border-radius: 24px;
  padding: 36px 24px 28px;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
  text-align: center;
  animation: slideUp 0.3s cubic-bezier(0.16, 1, 0.3, 1);
}

@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.back-btn {
  position: absolute;
  top: 12px;
  right: 12px;
  width: 32px;
  height: 32px;
  border: none;
  background: rgba(255, 255, 255, 0.3);
  border-radius: 50%;
  color: white;
  font-size: 18px;
  cursor: pointer;
  transition: all 0.2s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0;
  line-height: 1;
}

.back-btn:hover {
  background: rgba(255, 255, 255, 0.5);
  transform: scale(1.1);
}

.back-btn:active {
  transform: scale(0.95);
}

.customize-title {
  color: white;
  font-size: 24px;
  font-weight: 600;
  line-height: 28px;
  margin: 0 0 12px;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}

.customize-subtitle {
  color: rgba(255, 255, 255, 0.9);
  font-size: 13px;
  line-height: 18px;
  margin: 0 0 28px;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.15);
}

.plan-types {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
  margin-bottom: 24px;
}

.plan-type-btn {
  background: rgba(255, 255, 255, 0.25);
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-radius: 16px;
  padding: 16px 12px;
  color: white;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.2);
  min-height: 100px;
  justify-content: center;
}

.type-icon {
  font-size: 28px;
  display: block;
}

.type-name {
  line-height: 1.2;
}

.plan-type-btn:hover {
  background: rgba(255, 255, 255, 0.35);
  border-color: rgba(255, 255, 255, 0.5);
  transform: translateY(-2px);
}

.plan-type-active {
  background: rgba(255, 255, 255, 0.45) !important;
  border-color: white !important;
  box-shadow: 0 0 12px rgba(255, 255, 255, 0.3);
  transform: scale(1.05);
}

.plan-type-btn:active {
  transform: scale(0.98);
}

.confirm-btn {
  width: 100%;
  padding: 14px 16px;
  background: white;
  border: none;
  border-radius: 12px;
  color: #ff6b6b;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.confirm-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.2);
}

.confirm-btn:active {
  transform: translateY(0);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

/* Adapt for phone frame */
.phone-scroll .customize-page {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: 50;
}

.phone-scroll .customize-overlay {
  background: rgba(10, 10, 10, 0.7);
}
`

writeFileSync(file, c + customizeStyles, 'utf8')
console.log('✓ Added customize page styles')
