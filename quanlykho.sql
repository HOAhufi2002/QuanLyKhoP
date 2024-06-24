USE [quanlykhopho]
GO
/****** Object:  Table [dbo].[BaoCaoPhanTich]    Script Date: 24/06/2024 5:28:44 CH ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[BaoCaoPhanTich](
	[ID] [int] IDENTITY(1,1) NOT NULL,
	[NgayBaoCao] [date] NULL,
	[NoiDungBaoCao] [nvarchar](100) NULL,
	[MucTieuNguyenLieu] [nvarchar](100) NULL,
PRIMARY KEY CLUSTERED 
(
	[ID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[CongThucNauNuocDung]    Script Date: 24/06/2024 5:28:44 CH ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[CongThucNauNuocDung](
	[ID] [int] IDENTITY(1,1) NOT NULL,
	[TenCongThuc] [nvarchar](100) NOT NULL,
	[NguyenLieuID] [nvarchar](255) NULL,
	[PhuGiaGiaViID] [nvarchar](255) NULL,
	[PhuongPhap] [nvarchar](100) NULL,
PRIMARY KEY CLUSTERED 
(
	[ID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[MonAn]    Script Date: 24/06/2024 5:28:44 CH ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[MonAn](
	[ID] [int] IDENTITY(1,1) NOT NULL,
	[TenMonAn] [nvarchar](100) NOT NULL,
	[ThucDonID] [int] NULL,
	[MoTa] [nvarchar](255) NULL,
	[NguyenLieu] [nvarchar](255) NULL,
	[PhuGiaGiaVi] [nvarchar](255) NULL,
	[PhuongPhap] [nvarchar](255) NULL,
PRIMARY KEY CLUSTERED 
(
	[ID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[NguyenLieuPhoBo]    Script Date: 24/06/2024 5:28:44 CH ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[NguyenLieuPhoBo](
	[ID] [int] IDENTITY(1,1) NOT NULL,
	[TenNguyenLieu] [nvarchar](100) NOT NULL,
	[MoTa] [nvarchar](100) NULL,
	[DonViTinh] [nvarchar](100) NULL,
	[SoLuongTonKho] [float] NULL,
	[NgayHetHan] [date] NULL,
PRIMARY KEY CLUSTERED 
(
	[ID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[NhaCungCap]    Script Date: 24/06/2024 5:28:44 CH ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[NhaCungCap](
	[ID] [int] IDENTITY(1,1) NOT NULL,
	[TenNhaCungCap] [nvarchar](100) NOT NULL,
	[DiaChi] [nvarchar](255) NULL,
	[SoDienThoai] [nvarchar](20) NULL,
	[Email] [nvarchar](100) NULL,
	[LoaiNguyenLieu] [nvarchar](100) NULL,
PRIMARY KEY CLUSTERED 
(
	[ID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[NhaCungCap_NguyenLieu]    Script Date: 24/06/2024 5:28:44 CH ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[NhaCungCap_NguyenLieu](
	[NhaCungCapID] [int] NOT NULL,
	[NguyenLieuID] [int] NOT NULL,
PRIMARY KEY CLUSTERED 
(
	[NhaCungCapID] ASC,
	[NguyenLieuID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[PhuGiaGiaVi]    Script Date: 24/06/2024 5:28:44 CH ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[PhuGiaGiaVi](
	[ID] [int] IDENTITY(1,1) NOT NULL,
	[TenPhuGia] [nvarchar](100) NOT NULL,
	[MoTa] [nvarchar](100) NULL,
	[DonViTinh] [nvarchar](100) NULL,
	[SoLuongTonKho] [float] NULL,
	[NgayHetHan] [date] NULL,
PRIMARY KEY CLUSTERED 
(
	[ID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[TaiKhoan]    Script Date: 24/06/2024 5:28:44 CH ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[TaiKhoan](
	[ID] [int] IDENTITY(1,1) NOT NULL,
	[TenDangNhap] [nvarchar](50) NOT NULL,
	[MatKhau] [nvarchar](255) NOT NULL,
	[HoTen] [nvarchar](100) NULL,
	[Email] [nvarchar](100) NOT NULL,
	[Quyen] [nvarchar](50) NOT NULL,
	[NgayTao] [datetime] NULL,
PRIMARY KEY CLUSTERED 
(
	[ID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[ThucDon]    Script Date: 24/06/2024 5:28:44 CH ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[ThucDon](
	[ID] [int] IDENTITY(1,1) NOT NULL,
	[TenThucDon] [nvarchar](100) NOT NULL,
	[MoTa] [nvarchar](255) NULL,
PRIMARY KEY CLUSTERED 
(
	[ID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[TonKho]    Script Date: 24/06/2024 5:28:44 CH ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[TonKho](
	[ID] [int] IDENTITY(1,1) NOT NULL,
	[NguyenLieuID] [int] NULL,
	[PhuGiaID] [int] NULL,
	[SoLuongTon] [float] NULL,
PRIMARY KEY CLUSTERED 
(
	[ID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
SET IDENTITY_INSERT [dbo].[BaoCaoPhanTich] ON 

INSERT [dbo].[BaoCaoPhanTich] ([ID], [NgayBaoCao], [NoiDungBaoCao], [MucTieuNguyenLieu]) VALUES (1, CAST(N'2024-06-30' AS Date), N'Báo cáo tháng 6', N'Thịt bò: 50kg, Đường: 100kg')
INSERT [dbo].[BaoCaoPhanTich] ([ID], [NgayBaoCao], [NoiDungBaoCao], [MucTieuNguyenLieu]) VALUES (2, CAST(N'2024-07-31' AS Date), N'Báo cáo tháng 7', N'Gân bò: 20kg, Muối: 50kg')
INSERT [dbo].[BaoCaoPhanTich] ([ID], [NgayBaoCao], [NoiDungBaoCao], [MucTieuNguyenLieu]) VALUES (3, CAST(N'2024-08-31' AS Date), N'Báo cáo tháng 8', N'Hành: 30 bó, Nước mắm: 200 lít')
SET IDENTITY_INSERT [dbo].[BaoCaoPhanTich] OFF
GO
SET IDENTITY_INSERT [dbo].[CongThucNauNuocDung] ON 

INSERT [dbo].[CongThucNauNuocDung] ([ID], [TenCongThuc], [NguyenLieuID], [PhuGiaGiaViID], [PhuongPhap]) VALUES (10, N'Công thức thịt bò', N'Gân bò,Thịt bò,Hành', N'Muối,Đường', N'Phương nấu thịt bò rả đông')
INSERT [dbo].[CongThucNauNuocDung] ([ID], [TenCongThuc], [NguyenLieuID], [PhuGiaGiaViID], [PhuongPhap]) VALUES (12, N'a', N'Thịt bò, Gân bò', N'Nước mắm', N'a')
SET IDENTITY_INSERT [dbo].[CongThucNauNuocDung] OFF
GO
SET IDENTITY_INSERT [dbo].[MonAn] ON 

INSERT [dbo].[MonAn] ([ID], [TenMonAn], [ThucDonID], [MoTa], [NguyenLieu], [PhuGiaGiaVi], [PhuongPhap]) VALUES (4, N'Phở bò tái', 1, N'Phở bò tái với thịt bò tươi ngon', N'Thịt bò, Hành tây', N'Muối, Đường', N'Nấu nước dùng và chần thịt bò tái')
INSERT [dbo].[MonAn] ([ID], [TenMonAn], [ThucDonID], [MoTa], [NguyenLieu], [PhuGiaGiaVi], [PhuongPhap]) VALUES (5, N'Bún bò Huế', 2, N'Bún bò Huế với hương vị đặc trưng', N'Thịt bò, Hành tây, Tỏi', N'Muối, Nước mắm', N'Nấu nước dùng và bún bò')
INSERT [dbo].[MonAn] ([ID], [TenMonAn], [ThucDonID], [MoTa], [NguyenLieu], [PhuGiaGiaVi], [PhuongPhap]) VALUES (6, N'123', 2, N'123', N'Thịt bò, Gân bò', N'Đường, Muối', N'123')
INSERT [dbo].[MonAn] ([ID], [TenMonAn], [ThucDonID], [MoTa], [NguyenLieu], [PhuGiaGiaVi], [PhuongPhap]) VALUES (7, N'sấcc', 1, N'câcsc', N'Gân bò, Kim Chi', N'Muối', N'các')
INSERT [dbo].[MonAn] ([ID], [TenMonAn], [ThucDonID], [MoTa], [NguyenLieu], [PhuGiaGiaVi], [PhuongPhap]) VALUES (8, N'Kim Chi bò', 3, N'Kim chi ngon', N'Thịt bò, Gân bò', N'Đường', N'ok')
SET IDENTITY_INSERT [dbo].[MonAn] OFF
GO
SET IDENTITY_INSERT [dbo].[NguyenLieuPhoBo] ON 

INSERT [dbo].[NguyenLieuPhoBo] ([ID], [TenNguyenLieu], [MoTa], [DonViTinh], [SoLuongTonKho], [NgayHetHan]) VALUES (1, N'Thịt bò', N'Thịt bò tươi', N'kg', 50, CAST(N'2024-07-30' AS Date))
INSERT [dbo].[NguyenLieuPhoBo] ([ID], [TenNguyenLieu], [MoTa], [DonViTinh], [SoLuongTonKho], [NgayHetHan]) VALUES (2, N'Gân bò', N'Gân bò', N'kg', 20, CAST(N'2024-07-25' AS Date))
INSERT [dbo].[NguyenLieuPhoBo] ([ID], [TenNguyenLieu], [MoTa], [DonViTinh], [SoLuongTonKho], [NgayHetHan]) VALUES (3, N'Hành', N'Hành lá', N'bó', 30, CAST(N'2024-06-30' AS Date))
INSERT [dbo].[NguyenLieuPhoBo] ([ID], [TenNguyenLieu], [MoTa], [DonViTinh], [SoLuongTonKho], [NgayHetHan]) VALUES (6, N'phô mai', N'phô mai chua', N'kg', 100, CAST(N'2024-06-30' AS Date))
INSERT [dbo].[NguyenLieuPhoBo] ([ID], [TenNguyenLieu], [MoTa], [DonViTinh], [SoLuongTonKho], [NgayHetHan]) VALUES (7, N'Kim Chi', N'Kim Chi cay hàn quốc', N'kg', 100, CAST(N'2024-06-30' AS Date))
SET IDENTITY_INSERT [dbo].[NguyenLieuPhoBo] OFF
GO
SET IDENTITY_INSERT [dbo].[NhaCungCap] ON 

INSERT [dbo].[NhaCungCap] ([ID], [TenNhaCungCap], [DiaChi], [SoDienThoai], [Email], [LoaiNguyenLieu]) VALUES (1, N'Minh Hoa', N'hcm', N'03538390', N'123@gmail.com', N'Thịt bò')
SET IDENTITY_INSERT [dbo].[NhaCungCap] OFF
GO
SET IDENTITY_INSERT [dbo].[PhuGiaGiaVi] ON 

INSERT [dbo].[PhuGiaGiaVi] ([ID], [TenPhuGia], [MoTa], [DonViTinh], [SoLuongTonKho], [NgayHetHan]) VALUES (1, N'Đường', N'Đường cát trắng', N'kg', 100, CAST(N'2025-01-01' AS Date))
INSERT [dbo].[PhuGiaGiaVi] ([ID], [TenPhuGia], [MoTa], [DonViTinh], [SoLuongTonKho], [NgayHetHan]) VALUES (2, N'Muối', N'Muối tinh', N'kg', 50, CAST(N'2025-01-01' AS Date))
INSERT [dbo].[PhuGiaGiaVi] ([ID], [TenPhuGia], [MoTa], [DonViTinh], [SoLuongTonKho], [NgayHetHan]) VALUES (3, N'Nước mắm', N'Nước mắm cá cơm', N'lít', 200, CAST(N'2025-12-31' AS Date))
SET IDENTITY_INSERT [dbo].[PhuGiaGiaVi] OFF
GO
SET IDENTITY_INSERT [dbo].[TaiKhoan] ON 

INSERT [dbo].[TaiKhoan] ([ID], [TenDangNhap], [MatKhau], [HoTen], [Email], [Quyen], [NgayTao]) VALUES (23, N'hoa123123', N'123', N'Nguyễn Minh Hòa123', N'123@gmail.com', N'NhanVien', CAST(N'2024-06-24T08:20:06.000' AS DateTime))
INSERT [dbo].[TaiKhoan] ([ID], [TenDangNhap], [MatKhau], [HoTen], [Email], [Quyen], [NgayTao]) VALUES (24, N'admin', N'admin', N'123', N'hoahuit@gmail.com', N'Admin', CAST(N'2024-06-24T08:24:05.000' AS DateTime))
INSERT [dbo].[TaiKhoan] ([ID], [TenDangNhap], [MatKhau], [HoTen], [Email], [Quyen], [NgayTao]) VALUES (25, N'nhanvien', N'nhanvien', N'Nhanvien', N'nhanvien@gmail.com', N'NhanVien', CAST(N'2024-06-24T08:24:19.000' AS DateTime))
INSERT [dbo].[TaiKhoan] ([ID], [TenDangNhap], [MatKhau], [HoTen], [Email], [Quyen], [NgayTao]) VALUES (26, N'hoanv', N'123', N'Nguyễn Minh Hòa', N'hoahuit1@gmail.com', N'NhanVien', CAST(N'2024-06-24T08:28:48.000' AS DateTime))
SET IDENTITY_INSERT [dbo].[TaiKhoan] OFF
GO
SET IDENTITY_INSERT [dbo].[ThucDon] ON 

INSERT [dbo].[ThucDon] ([ID], [TenThucDon], [MoTa]) VALUES (1, N'Thực Đơn phở bò', N'Phở bò đặc biệt
')
INSERT [dbo].[ThucDon] ([ID], [TenThucDon], [MoTa]) VALUES (2, N'Gà hấp tiêu', N'Món gà được hấp tiêu đặc biệt')
INSERT [dbo].[ThucDon] ([ID], [TenThucDon], [MoTa]) VALUES (3, N'Kim Chi Hàn Quốc', N'ngon')
SET IDENTITY_INSERT [dbo].[ThucDon] OFF
GO
SET IDENTITY_INSERT [dbo].[TonKho] ON 

INSERT [dbo].[TonKho] ([ID], [NguyenLieuID], [PhuGiaID], [SoLuongTon]) VALUES (1, 1, NULL, 50)
INSERT [dbo].[TonKho] ([ID], [NguyenLieuID], [PhuGiaID], [SoLuongTon]) VALUES (2, NULL, 1, 100)
INSERT [dbo].[TonKho] ([ID], [NguyenLieuID], [PhuGiaID], [SoLuongTon]) VALUES (3, 2, 2, 20)
SET IDENTITY_INSERT [dbo].[TonKho] OFF
GO
SET ANSI_PADDING ON
GO
/****** Object:  Index [UQ__TaiKhoan__55F68FC043BE8412]    Script Date: 24/06/2024 5:28:45 CH ******/
ALTER TABLE [dbo].[TaiKhoan] ADD UNIQUE NONCLUSTERED 
(
	[TenDangNhap] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, IGNORE_DUP_KEY = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
GO
SET ANSI_PADDING ON
GO
/****** Object:  Index [UQ__TaiKhoan__A9D105342930809E]    Script Date: 24/06/2024 5:28:45 CH ******/
ALTER TABLE [dbo].[TaiKhoan] ADD UNIQUE NONCLUSTERED 
(
	[Email] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, IGNORE_DUP_KEY = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
GO
ALTER TABLE [dbo].[TaiKhoan] ADD  DEFAULT (getdate()) FOR [NgayTao]
GO
ALTER TABLE [dbo].[MonAn]  WITH CHECK ADD FOREIGN KEY([ThucDonID])
REFERENCES [dbo].[ThucDon] ([ID])
GO
ALTER TABLE [dbo].[NhaCungCap_NguyenLieu]  WITH CHECK ADD FOREIGN KEY([NguyenLieuID])
REFERENCES [dbo].[NguyenLieuPhoBo] ([ID])
GO
ALTER TABLE [dbo].[NhaCungCap_NguyenLieu]  WITH CHECK ADD FOREIGN KEY([NhaCungCapID])
REFERENCES [dbo].[NhaCungCap] ([ID])
GO
ALTER TABLE [dbo].[TonKho]  WITH CHECK ADD FOREIGN KEY([NguyenLieuID])
REFERENCES [dbo].[NguyenLieuPhoBo] ([ID])
GO
ALTER TABLE [dbo].[TonKho]  WITH CHECK ADD FOREIGN KEY([PhuGiaID])
REFERENCES [dbo].[PhuGiaGiaVi] ([ID])
GO
