export interface UserModel {
  id: number;
  firstName: string;
  lastName: string;
  userName: string;
  imgUrl: string;
  email: {
    name: string;
    verified: boolean;
  };
  phone: {
    number: string;
    verified: boolean;
  };
  sex: 'female' | 'male';
  birthday: string;
  lang: 'en' | 'de' | 'vi';
}

// export interface UserModel {
//   id: number;
//   firstName: string;
//   lastName: string;
//   imgUrl: string;
//   userName: string;
//   email: {
//     name: string;
//     verified: boolean;
//   };
//   phone: {
//     number: string;
//     verified: boolean;
//   };
//   sex: 'male' | 'female';
//   birthday: string;
//   lang: 'en' | 'de';
//   country: string;
//   city: string;
//   address1: string;
//   address2?: string;
//   zipcode: number;
//   website?: string;
//   socials?: {
//     twitter?: string;
//     facebook?: string;
//     linkedin?: string;
//   };
// }
