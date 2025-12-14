const moneyStyle = (denom) => {
  switch (denom) {
    case 1: // Copper
      return "invert(1) sepia(1) saturate(4) hue-rotate(20deg)"

    case 5: // Silver
      return "invert(1) grayscale(1) brightness(1.3)"

    case 10: // Gold
      return "invert(1) sepia(1) saturate(6) hue-rotate(45deg)"

    case 20: // Green banknote
      return "invert(1) sepia(1) saturate(3) hue-rotate(95deg)"

    case 50: // Blue banknote
      return "invert(1) sepia(1) saturate(2) hue-rotate(190deg)"

    case 100: // Red banknote
      return "invert(1) sepia(1) saturate(4) hue-rotate(330deg)"

    case 500: // Purple
      return "invert(1) sepia(1) saturate(3) hue-rotate(260deg)"

    case 1000: // Brown / Gold
      return "invert(1) sepia(1) saturate(3) hue-rotate(30deg)"

    default:
      return "invert(1)"
  }
};

export default moneyStyle;
