import React from 'react'
import { CListGroupItem, CBadge } from '@coreui/react'

const Ingredient = ({ ingredient, badgeColor, badgeText, children }) => {
  const isProcessed = ingredient.type === 'Processed'

  return (
    <CListGroupItem
      component={isProcessed ? 'button' : 'div'}
      {...(isProcessed ? { action: true } : {})}
      className="ingredient-item"
      draggable // Enable drag-and-drop
    >
      {ingredient.name}
      <CBadge color={badgeColor} className="ms-2" style={{ pointerEvents: 'none' }}>
        {badgeText}
      </CBadge>
      {children}
    </CListGroupItem>
  )
}

export default Ingredient
