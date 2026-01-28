import { Hand, AlertTriangle, CarCrash, ShieldAlert } from "lucide-react";

/**
 * CrimeIcon Component
 * Renders appropriate Lucide icon based on crime type
 * Used for reference and documentation
 */
export const CrimeIcon = ({ type, size = 18 }) => {
  const iconProps = {
    size,
    strokeWidth: 2.5,
  };

  switch (type?.toLowerCase()) {
    case "theft":
      return <Hand {...iconProps} />;
    case "assault":
      return <AlertTriangle {...iconProps} />;
    case "accident":
      return <CarCrash {...iconProps} />;
    default:
      return <ShieldAlert {...iconProps} />;
  }
};

export default CrimeIcon;
