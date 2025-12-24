import { axiosInstance } from "./axios-instance.ts";
import type { User } from "../types/user.ts";

export const getMe = async () => {
  const resonse = await axiosInstance.get<User>("/auth/me");
  return resonse.data;
};
