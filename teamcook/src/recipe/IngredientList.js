import React from 'react'
import { CListGroup } from '@coreui/react'
import RawIngredient from './RawIngredient'
import ProcessedIngredient from './ProcessedIngredient'

const IngredientList = ({ ingredients }) => {
  return (
    <CListGroup flush>
      {ingredients.map((ingredient, index) =>
        ingredient.type === 'Raw' ? (
          <RawIngredient key={index} ingredient={ingredient} />
        ) : (
          <ProcessedIngredient key={index} ingredient={ingredient} />
        ),
      )}
    </CListGroup>
  )
}

export default IngredientList
