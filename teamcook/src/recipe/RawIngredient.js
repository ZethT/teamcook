import Ingredient from './Ingredient' // Import the base Ingredient component

const RawIngredient = ({ ingredient }) => {
  return <Ingredient ingredient={ingredient} badgeColor="success" badgeText="RI" />
}

export default RawIngredient
